"""Main client for requesting API endpoints."""

from kuro.client.components import announcement, auth, gacha

__all__ = ["Client"]


class Client(auth.AuthClient, gacha.GachaClient, announcement.AnnouncementClient):
    """Main client for requesting API endpoints."""
