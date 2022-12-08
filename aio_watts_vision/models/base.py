"""Watts vision: Base"""
import logging 

class BaseObject():
    """Base class for Watts vision."""

    logger = logging.getLogger(__name__)

    def __init__(self, attributes) -> None:
        """Initialize."""
        self.attributes = attributes

class BaseAPIObject(BaseObject):
    """Base class for the Watts vision REST API."""

    def __init__(self, client: "AIOWattsVisionAPIClient", attributes: dict) -> None:
        """Initialise."""
        super().__init__(attributes)
        self.client = client        