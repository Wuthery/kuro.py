"""Main client for requesting API endpoints."""

from kuro.client.components import announcements, auth, gacha

__all__ = ["Client"]


class Client(
    auth.AuthClient,
    gacha.GachaClient,
    announcements.KurobbsAnnouncementClient,
    announcements.GameAnnouncementClient,
    announcements.LauncherAnnouncementClient,
):
    """Main client for requesting API endpoints."""
