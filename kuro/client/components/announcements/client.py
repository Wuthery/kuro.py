"""Announcements Client."""

from kuro.client.components.announcements import subclients


class AnnouncementsClient(subclients.GameAnnouncementClient, subclients.LauncherAnnouncementClient):
    """Announcements client."""
