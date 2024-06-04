"""Base client."""

from __future__ import annotations

import abc
import http.cookies
import json
import logging
import typing

import aiohttp
import yarl
from aiohttp_client_cache.backends.sqlite import SQLiteBackend
from aiohttp_client_cache.session import CachedSession

from ... import types

if typing.TYPE_CHECKING:
    import aiohttp.typedefs

CookieOrHeader = typing.Union[
    "http.cookies.BaseCookie[typing.Any]", typing.Mapping[typing.Any, typing.Any], str
]


def parse_cookie(cookie: CookieOrHeader | None) -> dict[str, str]:
    """Parse a cookie or header into a cookie mapping."""
    if cookie is None:
        return {}

    if isinstance(cookie, str):
        cookie = http.cookies.SimpleCookie(cookie)

    return {
        str(k): v.value if isinstance(v, http.cookies.Morsel) else str(v) for k, v in cookie.items()
    }


class BaseClient(abc.ABC):
    """Base client."""

    logger: logging.Logger = logging.getLogger(__name__)
    """Logger for the client."""

    _cookies: dict[str, str]
    """Cookies used for authentication."""

    def __init__(
        self,
        cookies: CookieOrHeader | None = None,
        *,
        lang: types.Lang = types.Lang.ENGLISH,
        debug: bool = False,
    ) -> None:
        self.cookies = parse_cookie(cookies) if cookies else {}
        self.lang = lang
        """Language to use for the API."""
        self.debug = debug
        """Whether to log debug information."""

    def _request_hook(
        self,
        method: str,
        url: aiohttp.typedefs.StrOrURL,
        *,
        params: typing.Mapping[str, typing.Any] | None = None,
        data: typing.Any = None,
        **_: typing.Any,
    ) -> None:
        """Perform an action before a request.

        Debug logging by default.
        """
        url = yarl.URL(url)
        if params:
            params = dict(params.items())
            url = url.update_query(params)

        if data:
            self.logger.debug("%s %s\n%s", method, url, json.dumps(data, separators=(",", ":")))
        else:
            self.logger.debug("%s %s", method, url)

    async def request(
        self,
        url: aiohttp.typedefs.StrOrURL,
        *,
        method: str | None = None,
        params: typing.Mapping[str, typing.Any] | None = None,
        data: typing.Any = None,
        headers: aiohttp.typedefs.LooseHeaders | None = None,
        **kwargs: typing.Any,
    ) -> typing.Mapping[str, typing.Any]:
        """Make a request to the API. All requests the library makes go through this method."""
        if method is None:
            method = "POST" if data else "GET"

        self._request_hook(method, url, params=params, data=data, headers=headers, **kwargs)

        cache = SQLiteBackend(cache_name=".cache/kuro-py")
        async with (
            CachedSession(cache=cache) as session,
            session.request(
                method,
                url,
                params=params,
                data=data,
                headers=headers,
                cookies=self.cookies,
                **kwargs,
            ) as response,
        ):
            data = await response.json()

        return data

    @property
    def cookies(self) -> typing.MutableMapping[str, str]:
        """Cookies used for authentication."""
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: CookieOrHeader | None) -> None:
        if not cookies:
            self._cookies = {}
            return

        self._cookies = parse_cookie(cookies)

    def set_cookies(
        self,
        cookies: CookieOrHeader | None = None,
        **kwargs: typing.Any,
    ) -> typing.MutableMapping[str, str]:
        """Parse and set cookies."""
        if not bool(cookies) ^ bool(kwargs):
            msg = "Cannot use both positional and keyword arguments at once"
            raise TypeError(msg)

        self.cookies = parse_cookie(cookies or kwargs)
        return self.cookies

    @property
    def debug(self) -> bool:
        """Whether the debug mode is enabled."""
        return logging.getLogger("kuro").level == logging.DEBUG

    @debug.setter
    def debug(self, debug: bool) -> None:
        logging.basicConfig()
        level = logging.DEBUG if debug else logging.NOTSET
        logging.getLogger("kuro").setLevel(level)
