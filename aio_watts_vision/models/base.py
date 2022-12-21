"""Watts vision: Base"""
import logging 

class BaseObject():
    """Base class for Watts vision."""

    logger = logging.getLogger(__name__)

    def __init__(self, attributes: dict) -> None:
        """Initialize."""
        self.attributes = attributes

class BaseAPIObject(BaseObject):
    """Base class for the Watts vision REST API."""
