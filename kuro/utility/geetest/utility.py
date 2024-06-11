"""Geetest utility functions."""

from kuro import constants, types

__all__ = ["lang_to_geetest_lang"]


def lang_to_geetest_lang(lang: types.Lang) -> str:
    """Convert API language to geetest lang."""
    return constants.GEETEST_LANGS.get(lang, "en")
