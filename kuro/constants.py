"""Constants for the lib."""

import typing

from kuro import types

__all__ = ["GEETEST_LANGS"]


GEETEST_LANGS: typing.Mapping[types.Lang, str] = {
    types.Lang.CHINESE_SIMPLIFIED: "zh-Hans",
    types.Lang.CHINESE_TRADITIONAL: "zh-Hant",
    types.Lang.ENGLISH: "en",
    types.Lang.JAPANESE: "ja",
    types.Lang.KOREAN: "ko",
    types.Lang.FRENCH: "fr",
    types.Lang.GERMAN: "de",
    types.Lang.SPANISH: "es",
}
"""Geetest languages."""

WUTHERY_CDN: str = "https://nogatekeep.wuthery.com"
"""Wuthery CDN URL."""
