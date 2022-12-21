from typing import List

from .auth import Auth
from .models.objects import SmarthomeData, User


class WattsVisionAPI:
    """Class to communicate with the ExampleHub API."""

    def __init__(self, auth: Auth):
        """Initialize the API and store the auth so we can make requests."""
        self.auth = auth

    async def async_get_user(self, username: str, lang="nl_NL") -> User:
        payload = {"token": "true", "email": username, "lang": "en_GB"}
        resp = await self.auth.request("post", "user/read", data=payload)
        return User((await resp.json())["data"])

    async def async_get_smarthome_data(self) -> SmarthomeData:
        """Return the smarthome data"""
        resp = await self.auth.request("get", "lights")
        resp.raise_for_status()
        return [SmarthomeData(smarthome_data, self.auth) for smarthome_data in await resp.json()]