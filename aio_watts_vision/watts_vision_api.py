from typing import List

from auth import Auth
from models.smarthome import Smarthome
from models.user import User
from models.enums import Language


class WattsVisionAPI:
    """Class to communicate with the ExampleHub API."""

    def __init__(self, auth: Auth):
        """Initialize the API and store the auth so we can make requests."""
        self.auth = auth

    async def async_get_user(self, username: str, lang=Language.ENGLISH.value) -> User:
        payload = {"token": "true", "email": username, "lang": lang}
        resp = await self.auth.request("post", "user/read", data=payload)
        resp.raise_for_status()
        return User((await resp.json())["data"], self.auth)

    async def async_get_smarthome_data(self, smarthome_id: str, lang=Language.ENGLISH.value) -> Smarthome:
        """Return the smarthome data"""
        payload = {"token": "true", "smarthome_id": smarthome_id, "lang": lang}
        resp = await self.auth.request("post", "smarthome/read", data=payload)
        resp.raise_for_status()
        return Smarthome((await resp.json())["data"], self.auth)