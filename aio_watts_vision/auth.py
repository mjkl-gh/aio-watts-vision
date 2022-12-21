from aiohttp import ClientSession, ClientResponse
from aio_watts_vision.abstract_auth import AbstractAuth

class Auth(AbstractAuth):
    def __init__(self, websession: ClientSession, host: str, token_manager):
        """Initialize the auth."""
        super().__init__(websession, host)
        self.token_manager = token_manager

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        if self.token_manager.is_token_valid():
            return self.token_manager.access_token
        token = await self.token_manager.refresh_access_token()
        return token