"""Lib exceptions and error handling logic."""

import typing

__all__ = ("KuroError",)


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
        self.api_msg = response.get("msg", "")

        self.retcode = self.retcode or RETCODES[self.api_msg]
        self.msg = self.msg or ERROR_TRANSLATIONS[self.retcode]

        super().__init__(self.msg)

    def __str__(self) -> str:
        return f"[{self.retcode}] {self.msg}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} retcode={self.retcode} msg={self.msg!r} api_msg={self.api_msg!r} response={self.response}"


# Example custom error class implementation:
# class CustomError(KuroError):
#     """Custom exception class."""

#     retcode = 35
#     msg = "Custom error"


RETCODES: typing.Mapping[str, int] = {
    "": 0,  # Unknown error
    "系统异常": 1,  # System error
}
"""Kuro.py's custom error codes matched with API error messages."""


ERROR_TRANSLATIONS: typing.Mapping[int, str] = {
    0: "Unknown error occurred when requesting the API",
    1: "System error",
}
"""English error messages translated from Kuro.py's custom error codes."""


def raise_from_data(data: typing.Mapping[str, typing.Any]) -> None:
    """Raise an exception from API data."""
    raise KuroError(data)
