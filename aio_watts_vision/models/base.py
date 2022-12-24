"""Watts vision: Base"""
import logging 
from auth import Auth

class BaseObject():
    """Base class for Watts vision."""

    logger = logging.getLogger(__name__)

    def __init__(self, attributes: dict) -> None:
        """Initialize."""
        self.attributes = attributes

class BaseAPIObject(BaseObject):
    """Base class for the Watts vision REST API."""

    def __init__(self, attributes: dict, auth: Auth) -> None:
        super().__init__(attributes)
        self.auth = auth
