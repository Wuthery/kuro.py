"""Main client for requesting API endpoints."""

from .components import auth

__all__ = ["Client"]


class Client(auth.AuthClient):
    """Main client for requesting API endpoints."""
