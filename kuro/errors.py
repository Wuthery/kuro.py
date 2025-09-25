"""Lib exceptions and error handling logic."""

import typing

__all__ = (
    "GeetestTriggeredError",
    "KuroError",
)


class KuroError(Exception):
    """Base exception class."""

    retcode: int = 0
    """Kuro.py's custom error code."""
    msg: str = ""
    """Translated error message."""
    api_msg: str = ""
    """Error message returned by the API."""
    response: typing.Mapping[str, typing.Any]
    """Original API response."""

    def __init__(self, response: typing.Mapping[str, typing.Any]) -> None:
        self.response = response
        self.api_msg = response.get("msg", response.get("message", ""))

        self.retcode = self.retcode or RETCODES[self.api_msg]
        self.msg = self.msg or ERROR_TRANSLATIONS[self.retcode]

        super().__init__(self.msg)

    def __str__(self) -> str:
        return f"[{self.retcode}] {self.msg}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} retcode={self.retcode} msg={self.msg!r} api_msg={self.api_msg!r} response={self.response}"


class GeetestTriggeredError(KuroError):
    """Geetest verification triggered error."""

    retcode = 41000
    msg = "Geetest verification triggered"


CUSTOM_ERRORS: typing.Mapping[int, type[KuroError]] = {
    41000: GeetestTriggeredError,
}
"""Mapping of kuro retcodes to custom error classes."""


RETCODES: typing.Mapping[str, int] = {
    "": 0,  # Unknown error
    "系统异常": 1,  # System error
    "请求游戏获取日志异常!": 2,  # Gacha history params expired
}
"""Kuro.py's custom error codes matched with API error messages."""


ERROR_TRANSLATIONS: typing.Mapping[int, str] = {
    0: "Unknown error occurred when requesting the API",
    1: "System error",
    2: "Gacha history params expired",
}
"""English error messages translated from Kuro.py's custom error codes."""


def raise_from_data(data: typing.Mapping[str, typing.Any]) -> None:
    """Raise an exception from API data."""
    code = data.get("code", data.get("codes"))
    if code in CUSTOM_ERRORS:
        raise CUSTOM_ERRORS[code](data)

    raise KuroError(data)
