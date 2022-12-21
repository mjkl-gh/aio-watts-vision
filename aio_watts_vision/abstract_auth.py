from aiohttp import ClientSession, ClientResponse
from abc import ABC, abstractmethod

class AbstractAuth(ABC):
    """Abstract class to make authenticated requests."""

    def __init__(self, websession: ClientSession, host: str):
        """Initialize the auth."""
        self.websession = websession
        self.host = host

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(self, method, url, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")
        data = kwargs.get("data")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)
        if data is None:
            data = {}
        else:
            data = dict(data)           

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"

        return await self.websession.request(
            method, f"{self.host}/{url}", headers=headers, data=data
        )
