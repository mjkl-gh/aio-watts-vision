from aiohttp import ClientSession, ClientResponse
from datetime import datetime, timedelta
import logging
from typing import Any, cast

from pprint import pprint

_LOGGER = logging.getLogger(__name__)

class TokenManager():
    websession: ClientSession
    url: str

    @classmethod
    async def create(self, websession: ClientSession, url: str, username: str, password: str):
        """Initialize the token manager."""
        freshTokenManager = TokenManager()
        freshTokenManager.websession = websession
        freshTokenManager.url = url
        await freshTokenManager.authenticate( username, password)
        return freshTokenManager

    async def _fetch_access_token(self, payload):
        _LOGGER.debug("Trying to get an access token.")
        async with self.websession.post(
            self.url,
            data=payload,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        ) as response:
            token = await response.json()
            if "access_token" not in token:
                raise Exception("No Somfy access token provided.")

            self._access_token = cast(str, token["access_token"])
            self._refresh_token = token["refresh_token"]
            self._expires_in = datetime.now() + timedelta(
                seconds=token["expires_in"] - 5
            )
            self._refresh_expires_in = datetime.now() + timedelta(
                seconds=token["refresh_expires_in"] - 5
            )
    
    async def authenticate(self, username: str, password: str):
        """Get the login token for the Watts Smarthome API"""

        payload = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": "app-front",
        }
        await self._fetch_access_token(payload)

    def is_token_valid(self) -> bool:
        return datetime.now() > self._expires_in

    def is_refresh_token_valid(self) -> bool:
        return datetime.now() > self._refresh_expires_in

    async def refresh_access_token(self) -> str:
        if not self.is_refresh_token_valid():
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": self._refresh_token,
                "client_id": "app-front",
            }
            await self._fetch_access_token(payload)
        return self._access_token

