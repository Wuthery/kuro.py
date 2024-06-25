"""Main client for requesting API endpoints."""

from kuro.client.components import announcements, auth, gacha, game

__all__ = ["Client"]


class Client(
    auth.AuthClient,
    gacha.GachaClient,
    game.GameClient,
    announcements.AnnouncementsClient,
):
    """Main client for requesting API endpoints."""
