"""Main client for requesting API endpoints."""

from .components import auth, gacha

__all__ = ["Client"]


class Client(auth.AuthClient, gacha.GachaClient):
    """Main client for requesting API endpoints."""
