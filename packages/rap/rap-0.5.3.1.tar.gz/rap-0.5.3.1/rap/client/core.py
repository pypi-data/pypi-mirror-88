import asyncio
import inspect
import logging
import msgpack
import random

from functools import wraps
from typing import Any, Callable, cast, Dict, List, Optional, Tuple, Type

from rap.client.model import Request, Response
from rap.common import exceptions as rap_exc
from rap.common.conn import Connection
from rap.common.exceptions import RPCError
from rap.common.middleware import BaseMiddleware
from rap.common.types import BASE_REQUEST_TYPE, BASE_RESPONSE_TYPE
from rap.common.utlis import Constant, Event, gen_random_str_id


__all__ = ["Client"]


class AsyncIteratorCall:
    """client support async iterator"""

    def __init__(self, method: str, client: "Client", *args: Tuple):
        self._method: str = method
        self._call_id: Optional[int] = None
        self._args = args
        self._client: "Client" = client

    def __aiter__(self):
        return self

    async def __anext__(self):
        """
        The server will return the call id of the generator function,
        and the client can continue to get data based on the call id.
        If no data, the server will return StopAsyncIteration or StopIteration error.
        """
        response: Response = await self._client.msg_request(self._method, *self._args, call_id=self._call_id)
        self._call_id = response.body["call_id"]
        return response.body["result"]


class Client:
    def __init__(
        self,
        timeout: int = 9,
        host: str = "localhost",
        port: int = 9000,
        keep_alive_time: int = 1200,
        ssl_crt_path: Optional[str] = None,
    ):
        self._conn = Connection(
            msgpack.Unpacker(raw=False, use_list=False),
            timeout,
            ssl_crt_path=ssl_crt_path,
        )
        self._msg_id: int = random.randrange(65535)
        self._future_dict: Dict[int, asyncio.Future] = {}
        self._listen_future: Optional[asyncio.Future] = None
        self._is_close: bool = True
        self._host: str = host
        self._port: int = port
        self._keep_alive_time: int = keep_alive_time
        self._timeout: int = timeout

        self._client_id: str = gen_random_str_id(8)
        self._declare_client_id: str = self._client_id

        self.rap_exc_dict = self._get_rap_exc_dict()

    #######################
    # support `async with`#
    #######################
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *args: Tuple):
        await self.wait_close()

    ##################
    # connect& close #
    ##################
    async def wait_close(self):
        """close client"""
        if self._is_close:
            raise RuntimeError("Client already closed")
        if self._conn.is_closed():
            raise ConnectionError("conn already closed")
        await self._drop_life_cycle()

        # close listen func
        self._is_close = True
        if not self._listen_future.cancelled():
            self._listen_future.cancel()
        self._listen_future = None
        logging.debug(f"close conn:{self._conn}")
        self._conn.close()

    async def connect(self, host: str = "localhost", port: int = 9000):
        """
        Create&conn connection;
        start listen response;
        send declare msg to server
        """
        if not self._conn.is_closed():
            raise ConnectionError(f"Client already connected")
        await self._conn.connect(host, port)
        logging.debug(f"Connection to %s...", self._conn.connection_info)
        self._is_close = False
        self._listen_future = asyncio.ensure_future(self._listen())
        await self._declare_life_cycle()

    ########
    # util #
    ########
    @staticmethod
    def raise_error(exc_name: str, exc_info: str = ""):
        """raise python exception"""
        exc = getattr(rap_exc, exc_name, None)
        if not exc:
            exc = globals()["__builtins__"][exc_name]
        if not exc:
            raise RPCError(exc_info)
        else:
            raise exc(exc_info)

    @staticmethod
    def _get_rap_exc_dict() -> Dict[int, Type[rap_exc.BaseRapError]]:
        exc_dict: Dict[int, Type[rap_exc.BaseRapError]] = {}
        for exc_name in dir(rap_exc):
            class_: Type = getattr(rap_exc, exc_name)
            if (
                inspect.isclass(class_)
                and issubclass(class_, rap_exc.BaseRapError)
                and class_.__name__ != rap_exc.BaseRapError.__class__.__name__
            ):
                exc_dict[class_.status_code] = class_
        return exc_dict

    def load_middleware(self, middleware_list: List[BaseMiddleware]):
        for middleware in middleware_list:
            if isinstance(middleware, BaseMiddleware):
                middleware.load_sub_middleware(self._real_base_request)
                self._real_base_request = middleware
            else:
                raise RuntimeError(f"{middleware} must be instance {BaseMiddleware}")

    async def _listen(self):
        """listen server msg"""
        logging.debug(f"listen:%s start", self._conn)
        try:
            while not self._is_close:
                await self._base_response()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            logging.exception(f"listen status:{self._is_close} error: {e}, close conn:{self._conn}")
            if not self._conn.is_closed():
                self._conn.close()

    ##############
    # life cycle #
    ##############
    async def _declare_life_cycle(self):
        """send declare msg and init client id"""
        body: dict = {}
        self._client_id = self._declare_client_id
        request: Request = Request(Constant.DECLARE_REQUEST, body)
        response = await self._base_request(request)
        if response.num != Constant.DECLARE_RESPONSE and response.body != body:
            raise RPCError("declare response error")
        client_id = response.body.get("client_id")
        if client_id is None:
            raise RPCError("declare response error, Can not get client id from body")
        self._client_id = client_id
        logging.info("declare success")

    async def _drop_life_cycle(self):
        """send drop msg"""
        call_id: str = gen_random_str_id(8)
        request: Request = Request(Constant.DROP_REQUEST, {"call_id": call_id})
        response = await self._base_request(request)
        if response.num != Constant.DROP_RESPONSE and response.body.get("call_id", "") != call_id:
            logging.warning("drop response error")
        else:
            logging.info("drop response success")

    def before_request_handle(self, request: Request):
        """check conn and header"""
        if self._conn.is_closed():
            raise ConnectionError("The connection has been closed, please call connect to create connection")

        def set_header_value(header_key: str, header_Value: Any):
            """set header value"""
            if header_key not in request.header:
                request.header[header_key] = header_Value

        set_header_value("client_id", self._client_id)
        set_header_value("version", Constant.VERSION)
        set_header_value("user_agent", Constant.USER_AGENT)

    # request&response
    async def _base_request(self, request: Request) -> Response:
        self.before_request_handle(request)
        return await self._real_base_request(request)

    async def _send(self, request: Request, msg_id: int):
        request: BASE_REQUEST_TYPE = (request.num, msg_id, request.header, request.body)
        try:
            await self._conn.write(request)
            logging.debug(f"send:%s to %s", request, self._conn.connection_info)
        except asyncio.TimeoutError as e:
            logging.error(f"send to %s timeout, drop data:%s", self._conn.connection_info, request)
            raise e
        except Exception as e:
            raise e

    async def _real_base_request(self, request: Request) -> Response:
        """gen msg id, send and recv response"""
        msg_id: int = self._msg_id + 1
        # Avoid too big numbers
        if msg_id > 65535:
            msg_id = 1
        self._msg_id = msg_id

        await self._send(request, msg_id)

        try:
            self._future_dict[msg_id] = asyncio.Future()
            try:
                return await asyncio.wait_for(self._future_dict[msg_id], self._timeout)
            except asyncio.TimeoutError:
                raise asyncio.TimeoutError(f"msg_id:{msg_id} request timeout")
        finally:
            if msg_id in self._future_dict:
                del self._future_dict[msg_id]

    async def _base_response(self):
        """recv server msg handle"""
        try:
            response: Optional[BASE_RESPONSE_TYPE] = await self._conn.read(self._keep_alive_time)
            logging.debug(f"recv raw data: %s", response)
        except asyncio.TimeoutError as e:
            logging.error(f"recv response from {self._conn.connection_info} timeout")
            self._conn.set_reader_exc(e)
            raise e
        except asyncio.CancelledError:
            return
        except Exception as e:
            self._conn.set_reader_exc(e)
            raise e

        if response is None:
            raise ConnectionError("Connection has been closed")
        # parse response
        try:
            response_num, msg_id, header, body = response
        except ValueError:
            logging.error(f"recv wrong response:{response}")
            return

        # server error response handle
        if response_num == Constant.SERVER_ERROR_RESPONSE:
            status_code: int = header.get("status_code", 500)
            exc: Type["rap_exc.BaseRapError"] = self._get_rap_exc_dict().get(status_code, rap_exc.BaseRapError)
            self._future_dict[msg_id].set_exception(exc(body))
            return

        # server event msg handle
        if response_num == Constant.SERVER_EVENT:
            event, event_info = body
            if event == Constant.EVENT_CLOSE_CONN:
                raise RuntimeError(f"recv close conn event, event info:{event_info}")
            elif event == Constant.PING_EVENT:
                request: Request = Request(Constant.CLIENT_EVENT_RESPONSE, Event(Constant.PONG_EVENT, "").to_tuple())
                self.before_request_handle(request)
                await self._send(request, msg_id=-1)
                return

        # set msg to future_dict's `future`
        if msg_id not in self._future_dict:
            logging.error(f"recv msg_id: {msg_id} error, client not request msg id:{msg_id}")
            return
        self._future_dict[msg_id].set_result(Response(response_num, msg_id, header, body))

    async def msg_request(self, method, *args, call_id=-1) -> Response:
        """msg request handle"""
        request: Request = Request(Constant.MSG_REQUEST, {"call_id": call_id, "method_name": method, "param": args})
        response: Response = await self._base_request(request)
        if response.num != Constant.MSG_RESPONSE:
            raise RPCError("request num error")
        if "exc" in response.body:
            if response.header.get("user_agent") == Constant.USER_AGENT:
                self.raise_error(response.body["exc"], response.body.get("exc_info", ""))
            else:
                raise RuntimeError(response.body.get("ext_info", ""))
        return response

    # register
    def _async_register(self, func: Callable):
        """Decorate normal function"""

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await self.raw_call(func.__name__, *args)

        return cast(Callable, wrapper)

    def _async_gen_register(self, func: Callable):
        """Decoration generator function"""

        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            async for result in self.iterator_call(func.__name__, *args):
                yield result

        return cast(Callable, wrapper)

    # client api
    async def raw_call(self, method: str, *args: Any) -> Any:
        """rpc client base call method"""
        response = await self.msg_request(method, *args)
        return response.body["result"]

    async def call(self, func: Callable, *args: Any) -> Any:
        """automatically resolve function names and call call_by_text"""
        return await self.raw_call(func.__name__, *args)

    async def iterator_call(self, method: str, *args: Any) -> Any:
        """Python-specific generator call"""
        async for result in AsyncIteratorCall(method, self, *args):
            yield result

    def register(self, func: Callable) -> Any:
        """Using this method to decorate a fake function can help you use it better.
        (such as ide completion, ide reconstruction and type hints)"""
        if inspect.iscoroutinefunction(func):
            return self._async_register(func)
        elif inspect.isasyncgenfunction(func):
            return self._async_gen_register(func)
