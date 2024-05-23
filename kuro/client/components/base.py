"""Base client."""

import abc
import json
import http.cookies
import logging
import typing
import yarl

import aiohttp

from ... import types


CookieOrHeader = typing.Union[
    "http.cookies.BaseCookie[typing.Any]", typing.Mapping[typing.Any, typing.Any], str
]


def parse_cookie(cookie: typing.Optional[CookieOrHeader]) -> typing.Dict[str, str]:
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

    _cookies: typing.Dict[str, str]
    """Cookies used for authentication."""

    def __init__(
        self,
        cookies: typing.Optional[CookieOrHeader] = None,
        *,
        lang: types.Lang = types.Lang.ENGLISH,
        debug: bool = False,
    ) -> None:
        self.cookies = parse_cookie(cookies) if cookies else {}
        self.lang = lang
        """Language to use for the API."""
        self.debug = debug
        """Whether to log debug information."""

    async def _request_hook(
        self,
        method: str,
        url: aiohttp.typedefs.StrOrURL,
        *,
        params: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        data: typing.Any = None,
        **kwargs: typing.Any,
    ) -> None:
        """Perform an action before a request.

        Debug logging by default.
        """
        url = yarl.URL(url)
        if params:
            params = {k: v for k, v in params.items()}
            url = url.update_query(params)

        if data:
            self.logger.debug("%s %s\n%s", method, url, json.dumps(data, separators=(",", ":")))
        else:
            self.logger.debug("%s %s", method, url)

    async def request(
        self,
        url: aiohttp.typedefs.StrOrURL,
        *,
        method: typing.Optional[str] = None,
        params: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        data: typing.Any = None,
        headers: typing.Optional[aiohttp.typedefs.LooseHeaders] = None,
        **kwargs: typing.Any,
    ) -> typing.Mapping[str, typing.Any]:
        """Make a request to the API. All requests the library makes go through this method."""

        # TODO: Implement getting data from cache here

        if "json" in kwargs:
            raise TypeError("Use data instead of json in request.")

        if method is None:
            method = "POST" if data else "GET"

        await self._request_hook(method, url, params=params, data=data, headers=headers, **kwargs)

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url,
                params=params,
                data=data,
                headers=headers,
                cookies=self.cookies,
                **kwargs,
            ) as response:
                data = await response.json()

        # TODO: Implement setting data to cache here

        return data

    @property
    def cookies(self) -> typing.MutableMapping[str, str]:
        """Cookies used for authentication."""
        return self._cookies

    @cookies.setter
    def cookies(self, cookies: typing.Optional[CookieOrHeader]) -> None:
        if not cookies:
            self._cookies = {}
            return

        self._cookies = parse_cookie(cookies)

    def set_cookies(
        self,
        cookies: typing.Optional[CookieOrHeader] = None,
        **kwargs: typing.Any,
    ) -> typing.MutableMapping[str, str]:
        """Parse and set cookies."""
        if not bool(cookies) ^ bool(kwargs):
            raise TypeError("Cannot use both positional and keyword arguments at once")

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
