"""Lib exceptions and error handling logic."""

import typing


class KuroException(Exception):
    """Base exception class."""

    retcode: int = 0
    """Kuro.py's custom error code."""
    msg: str = ""
    """Translated error message."""
    response: typing.Mapping[str, typing.Any] = {}
    """Original API response."""

    def __init__(self, response: typing.Mapping[str, typing.Any]) -> None:
        m = response.get("msg", "")

        self.response = response
        self.retcode = self.retcode or RETCODES.get(m, 0)
        self.msg = f"[{self.retcode}] " + (self.msg or ERROR_TRANSLATIONS.get(self.retcode))

        super().__init__(self.msg)


RETCODES: typing.Mapping[str, int] = {
    "": 0,  # Unknown error
    "系统异常": 1,  # System error
}
"""Kuro.py's custom error codes matched with API error messages."""


ERROR_TRANSLATIONS: typing.Mapping[int, str] = {
    0: "Unknown error occurred when requesting the API",
    1: "System error"
}
"""English error messages translated from Kuro.py's custom error codes."""


def raise_from_data(data: typing.Mapping[str, typing.Any]) -> None:
    """Raise an exception from API data."""
    raise KuroException(data)
