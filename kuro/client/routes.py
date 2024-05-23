"""All API endpoints in one place."""

import abc
import yarl

__all__ = ["GET_SMS_CODE", "WEB_LOGIN", "Route"]


class BaseRoute(abc.ABC):
    """Base route class."""


class Route(BaseRoute):
    """Standard route."""

    url: yarl.URL

    def __init__(self, url: str) -> None:
        self.url = yarl.URL(url)

    def get_url(self) -> yarl.URL:
        """Get the route URL."""
        return self.url


GET_SMS_CODE = Route("https://api.kurobbs.com/user/getSmsCodeForH5")

WEB_LOGIN = Route("https://api.kurobbs.com/user/loginForH5")