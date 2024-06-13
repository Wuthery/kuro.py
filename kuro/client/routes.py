"""All API endpoints in one place."""

import yarl

__all__ = ["GACHA_RECORD_URL", "GET_SMS_CODE", "WEB_LOGIN", "Route"]


class Route:
    """Standard route."""

    url: yarl.URL

    def __init__(self, url: str) -> None:
        self.url = yarl.URL(url)

    def get_url(self) -> yarl.URL:
        """Get the route URL."""
        return self.url


GACHA_RECORD_URL = Route("https://gmserver-api.aki-game2.net/gacha/record/query")

GET_SMS_CODE = Route("https://api.kurobbs.com/user/getSmsCodeForH5")

WEB_LOGIN = Route("https://api.kurobbs.com/user/loginForH5")

GAME_ANNOUNCEMENTS = Route(
    "https://aki-gm-resources-back.aki-game.net/gamenotice/G153/6eb2a235b30d05efd77bedb5cf60999e/notice.json"
)

GAME_ANNOUNCEMENT_DETAILS = Route(
    "https://aki-gm-resources-back.aki-game.net/gamenotice/content/G153/6eb2a235b30d05efd77bedb5cf60999e/"
)
