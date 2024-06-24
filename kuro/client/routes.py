"""All API endpoints in one place."""

import typing

import yarl

from kuro import types

__all__ = ["GACHA_RECORD_URL", "GET_SMS_CODE", "WEB_LOGIN", "Route"]


class Route:
    """Standard route."""

    url: yarl.URL

    def __init__(self, url: str) -> None:
        self.url = yarl.URL(url)

    def get_url(self) -> yarl.URL:
        """Get the route URL."""
        return self.url


class InternationalRoute:
    """Standard international route."""

    urls: typing.Mapping[types.Region, yarl.URL]

    def __init__(self, *, overseas: str, chinese: str) -> None:
        self.urls = {
            types.Region.OVERSEAS: yarl.URL(overseas),
            types.Region.CHINESE: yarl.URL(chinese),
        }

    def get_url(self, region: types.Region) -> yarl.URL:
        """Attempt to get a URL."""
        if not self.urls[region]:
            raise RuntimeError(f"URL does not support {region.name} region.")

        return self.urls[region]


GACHA_RECORD_URL = Route("https://gmserver-api.aki-game2.net/gacha/record/query")

GET_SMS_CODE = Route("https://api.kurobbs.com/user/getSmsCodeForH5")

WEB_LOGIN = Route("https://api.kurobbs.com/user/loginForH5")

GAME_ANNOUNCEMENTS = InternationalRoute(
    overseas="https://aki-gm-resources-back.aki-game.net/gamenotice/G153/6eb2a235b30d05efd77bedb5cf60999e/notice.json",
    chinese="https://aki-gm-resources-back.aki-game.com/gamenotice/G152/76402e5b20be2c39f095a152090afddc/notice.json",
)

GAME_ANNOUNCEMENT_DETAILS = InternationalRoute(
    overseas="https://aki-gm-resources-back.aki-game.net/gamenotice/content/G153/6eb2a235b30d05efd77bedb5cf60999e/",
    chinese="https://aki-gm-resources-back.aki-game.com/gamenotice/content/G152/76402e5b20be2c39f095a152090afddc/",
)

LAUNCHER_ANNOUNCEMENT_LIST = InternationalRoute(
    overseas="https://hw-pcdownload-qcloud.aki-game.net/pcstarter/prod/starter/50004_obOHXFrFanqsaIEOmuKroCcbZkQRBC7c/G153/guidance/",
    chinese="https://pcdownload-huoshan.aki-game.com/pcstarter/prod/starter/10003_Y8xXrXk65DqFHEDgApn3cpK5lfczpFx5/G152/guidance/zh-Hans.json",
)

LAUNCHER_ANNOUNCEMENT_DETAILS = InternationalRoute(
    overseas="https://hw-media-cdn-mingchao.kurogame.com/akiwebsite/website2.0/json/G152/",
    chinese="https://media-cdn-mingchao.kurogame.com/akiwebsite/website2.0/json/G152/",
)
