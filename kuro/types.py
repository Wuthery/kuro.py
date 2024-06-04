"""Types used in the library."""

import enum

__all__ = ["Game", "Lang"]


class Game(enum.StrEnum):
    """Kuro game."""

    PGR = "pgr"
    """Punishing: Gray Raven"""

    WUWA = "wuwa"
    """Wuthering Waves"""


class Lang(enum.StrEnum):
    """Languages supported by the API."""

    CHINESE_SIMPLIFIED = "zh-Hans"
    CHINESE_TRADITIONAL = "zh-Hant"
    ENGLISH = "en"
    JAPANESE = "ja"
    KOREAN = "ko"
    FRENCH = "fr"
    GERMAN = "de"
    SPANISH = "es"


class WuWaServer(enum.StrEnum):
    """WuWa server."""

    AMERICA = "591d6af3a3090d8ea00d8f86cf6d7501"
    """America"""

    ASIA = "86d52186155b148b5c138ceb41be9650"
    """Asia"""

    EUROPE = "6eb2a235b30d05efd77bedb5cf60999e"
    """Europe"""

    HMT = "919752ae5ea09c1ced910dd668a63ffb"
    """Hong Kong, Macau, Taiwan"""

    SEA = "10cd7254d57e58ae560b15d51e34b4c8"
    """Southeast Asia"""


class WuWaBanner(enum.IntEnum):
    """WuWa banner."""

    FEATURED_RESONATOR = 1
    """Featured Resonator Convene"""

    FEATURED_WEAPON = 2
    """Featured Weapon Convene"""

    STANDARD_RESONATOR = 3
    """"Standard Resonator Convene"""

    STANDARD_WEAPON = 4
    """Standard Weapon Convene"""

    BEGINNERS = 5
    """Beginner's Convene"""

    BEGINNERS_CHOICE = 6
    """Beginner's Choice Convene"""

    GIVEBACK_CUSTOM = 7
    """Beginner's Choice Convene (Giveback Custom Convene)"""
