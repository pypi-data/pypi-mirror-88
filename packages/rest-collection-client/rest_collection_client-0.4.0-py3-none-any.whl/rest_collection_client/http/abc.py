from abc import ABCMeta, abstractmethod
from asyncio import Lock, Semaphore, gather, wait
from typing import Any, Coroutine, MutableMapping, Optional, \
    Tuple, Union

from aiohttp import ClientResponse, \
    ClientResponseError, ClientSession, ContentTypeError
from aiohttp.typedefs import StrOrURL
from ujson import dumps
from yarl import URL

from rest_collection_client.typing import JsonContentOrText
from .container import ClientResponseContextManager, HttpClientExcData
from .exc import AIOHTTP_EXCEPTION_MAP, HttpClientAuthenticationError, \
    HttpClientAuthorizationError, HttpClientRequestError, \
    HttpClientResponseContentError, HttpClientResponseError
from .mixin import HttpClientAllMethodsMixin, HttpClientGetMethodMixin

__all__ = [
    'AbstractHttpClient',
    'AbstractGetHttpClient',
    'AbstractAllMethodsHttpClient',
    'AbstractChunkedGetHttpClient',
    'AbstractAuthenticatedChunkedGetHttpClient',
]


_DEFAULT_CONCURRENT_REQUEST_QUANTITY = 10


def _remove_raise_for_status_param(params: MutableMapping[str, Any]) -> None:
    params.pop('raise_for_status', None)


class AbstractHttpClient(metaclass=ABCMeta):
    """Abstract class-based http client."""

    def __init__(
        self,
        session: ClientSession,
        *args: Any,  # noqa
        **kwargs: Any,  # noqa
    ) -> None:
        self._session = session

    @classmethod
    def with_own_session(
        cls,
        *args: Any,
        session_params: Optional[MutableMapping[str, Any]] = None,
        **kwargs,
    ) -> 'AbstractHttpClient':
        # Delete raise for status option, handle statuses manualy.
        if session_params is None:
            session_params = {}

        _remove_raise_for_status_param(session_params)

        return cls(
            ClientSession(
                json_serialize=dumps,
                raise_for_status=False,
                **session_params,
            ),
            *args,
            **kwargs,
        )

    def close(self) -> Coroutine[None, None, None]:
        return self._session.close()

    @abstractmethod
    async def _request(self,
                       method: str,
                       url: StrOrURL,
                       *args: Any,
                       **kwargs: Any) -> Any: ...

    async def __aenter__(self) -> 'AbstractHttpClient':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()


class AbstractGetHttpClient(HttpClientGetMethodMixin, AbstractHttpClient):
    """Abstract http client for GET requests only."""

    @abstractmethod
    async def _request(self,
                       method: str,
                       url: StrOrURL,
                       *args,
                       **kwargs: Any) -> Any: ...


class AbstractAllMethodsHttpClient(HttpClientAllMethodsMixin,
                                   AbstractGetHttpClient):
    """Abstract http client for all request types."""
    @abstractmethod
    async def _request(self,
                       method: str,
                       url: StrOrURL,
                       *args,
                       **kwargs: Any) -> Any: ...


def _raise_for_status(resp: ClientResponse,
                      exc_data: Optional = None) -> None:
    """Raise for status wrapper."""
    try:
        resp.raise_for_status()

    except ClientResponseError as err:

        if resp.status == 401:
            raise HttpClientAuthenticationError(data=exc_data) from err

        elif resp.status == 403:
            raise HttpClientAuthorizationError(data=exc_data) from err

        raise HttpClientResponseContentError(data=exc_data) from err


class AbstractChunkedGetHttpClient(AbstractGetHttpClient):
    """Abstract http client for GET requests by chunks for performance and
    memory optimization purporses."""
    def __init__(
        self,
        *args: Any,
        max_concurrent_request_quantity: int =
        _DEFAULT_CONCURRENT_REQUEST_QUANTITY,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self._semaphore = Semaphore(max_concurrent_request_quantity)

    async def get_chunked(self,
                          url: StrOrURL,
                          *args,
                          chunk_size: int = 100,
                          **kwargs) -> Tuple[JsonContentOrText, ...]:
        # Firstly, we should read first chunk, because we dont know how many
        # chunks should we request at all.
        first_chunk_url = self._compose_first_chunk_url(url, chunk_size)

        first_chunk = await self.get(first_chunk_url, *args, **kwargs)

        # We have first chunk, we can calculate other chunk urls by it`s
        # metadata.
        other_chunk_urls = self._compose_other_chunk_urls(
            url, chunk_size, first_chunk
        )

        get_chunk_coros = tuple(
            self.get(chunk_url, **kwargs) for chunk_url in other_chunk_urls
        )
        gather_future = gather(*get_chunk_coros)

        try:
            return first_chunk, *await gather_future

        except Exception:
            # Exception occurs in one of coros, but other coros should be
            # cancelled and waited for ending.
            gather_future.cancel()
            await wait(get_chunk_coros)

            raise

    async def _request_concurrent(self,
                                  method: str,
                                  url: Union[str, URL],
                                  raise_for_status: bool = False,
                                  **params) -> ClientResponse:

        try:
            async with self._semaphore:
                return await self._session.request(
                    method,
                    url,
                    raise_for_status=raise_for_status,
                    **params,
                )

        except Exception as err:
            # todo: handle 401 and 403 statuses separately.
            exc_cls = AIOHTTP_EXCEPTION_MAP.get(
                type(err), HttpClientRequestError
            )
            raise exc_cls(data=HttpClientExcData(url, method, params)) from err

    async def _request(self,
                       method: str,
                       url: StrOrURL,
                       *args,
                       **kwargs) -> Union[JsonContentOrText, bytes]:
        _remove_raise_for_status_param(kwargs)

        with ClientResponseContextManager(
            await self._request_concurrent(
                method,
                url,
                raise_for_status=False,
                **kwargs,
            )
        ) as resp:

            exc_data = HttpClientExcData(url, method, kwargs)
            _raise_for_status(resp, exc_data)

            try:
                content_type = resp.headers.get('content-type')

                if content_type is None:
                    return await resp.read()

                # https://www.ietf.org/rfc/rfc2045.txt
                # Content Type string can contain additional params like charset
                if content_type.startswith('application/json'):
                    # Server responsed with json, let's read it.
                    return await resp.json()

                if content_type.startswith('text/'):
                    # Server responsed with text, let's read it.
                    return await resp.text()

                return await resp.read()

            except ContentTypeError as err:
                raise HttpClientResponseError(data=exc_data) from err

            except Exception as err:
                raise HttpClientResponseContentError(data=exc_data) from err

    @abstractmethod
    def _compose_other_chunk_urls(self,
                                  url: StrOrURL,
                                  chunk_size: int,
                                  first_chunk: JsonContentOrText) -> str:
        """Generate urls to request other chunks."""

    @abstractmethod
    def _compose_first_chunk_url(self,
                                 url: StrOrURL,
                                 chunk_size: int) -> str:
        """Generate first chunk url."""


class AbstractAuthenticatedChunkedGetHttpClient(AbstractChunkedGetHttpClient):
    """Abstract class for http client for GET chunked requests with
    authentication."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._authenticated = False
        self._authenticated_lock = Lock()

    @abstractmethod
    def _compose_other_chunk_urls(self,
                                  url: StrOrURL,
                                  chunk_size: int,
                                  first_chunk: JsonContentOrText) -> str: ...

    @abstractmethod
    def _compose_first_chunk_url(self,
                                 url: StrOrURL,
                                 chunk_size: int) -> str: ...

    async def _check_authentication(self, authentication_data: Any) -> bool:
        """Checking authentication flag or get authentication."""
        async with self._authenticated_lock:
            if self._authenticated:
                return True

            # We cannot release lock, otherwise, anyone else can aquire this
            # lock again and check authentication, find, that it is
            # falsy, and start authentication request too.
            authenticated = await self._request_authentication(
                authentication_data
            )
            self._authenticated = authenticated
            return authenticated

    async def _clear_authentication(self) -> None:
        """Clear authentication flag and data."""
        async with self._authenticated_lock:
            await self._erase_authentication_data()
            self._authenticated = False

    @abstractmethod
    async def _request_authentication(self, authentication_data: Any) -> bool:
        """Making authentication request."""

    @abstractmethod
    async def _erase_authentication_data(self) -> None:
        """Clear session authentication information."""

    async def _request(self,  # noqa
                       method: str,
                       url: StrOrURL,
                       authentication_data: Any,
                       *args,
                       **kwargs) -> Union[JsonContentOrText, bytes]:
        authenticated = await self._check_authentication(authentication_data)

        if not authenticated:
            raise HttpClientAuthenticationError(
                data=HttpClientExcData(url, method, kwargs)
            )

        try:
            return await super()._request(method, url, *args, **kwargs)

        except (HttpClientAuthenticationError, HttpClientAuthorizationError):
            # May be, authentication data was expired, but flag is set, we need
            # request authentication again.
            await self._clear_authentication()
            authenticated = await self._check_authentication(
                authentication_data
            )

            if not authenticated:
                raise

            # We cannot await coro again, thats why we didn`t assign
            # expression ``super()._request(method, url, *args, **kwargs)``
            # to variable before try/except block.
            return await super()._request(method, url, *args, **kwargs)
