"""Types used in the library."""

import enum

__all__ = ["Game", "Lang"]


class Game(str, enum.Enum):
    """Kuro game."""

    PGR = "pgr"
    """Punishing: Gray Raven"""

    WUWA = "wuwa"
    """Wuthering Waves"""


class Lang(str, enum.Enum):
    """Languages supported by the API."""

    CHINESE_SIMPLIFIED = "zh-Hans"
    CHINESE_TRADITIONAL = "zh-Hant"
    ENGLISH = "en"
    JAPANESE = "ja"
    KOREAN = "ko"
    FRENCH = "fr"
    GERMAN = "de"
    SPANISH = "es"
