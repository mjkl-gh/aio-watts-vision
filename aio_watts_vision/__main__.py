import asyncio
import aiohttp
import logging
from pprint import pprint

from token_manager import TokenManager
from auth import Auth
from models.enums import Mode
from models.smarthome import Smarthome
from watts_vision_api import WattsVisionAPI

_LOGGER = logging.getLogger(__name__)

_LOGGER.setLevel("DEBUG")

USERNAME = 
PASSWORD = 

WATTS_VISION_URL = "https://smarthome.wattselectronics.com" 
WATTS_VISION_AUTH_URL = WATTS_VISION_URL + "/auth/realms/watts/protocol/openid-connect/token"
WATTS_VISION_API_URL = WATTS_VISION_URL + "/api/v0.1/human"

_LOGGER = logging.getLogger(__name__)


async def main():
    async with aiohttp.ClientSession() as session:
        token_manager = await TokenManager.create(session,  WATTS_VISION_AUTH_URL, USERNAME, PASSWORD)
        auth = Auth(session, WATTS_VISION_API_URL, token_manager)
        api= WattsVisionAPI(auth)

        user = await api.async_get_user(USERNAME)
        pprint(vars(user))

        while True:
            smarthome_data = await api.async_get_smarthome_data(user.smarthomes[0].smarthome_id)
            print("Smarthome object:")
            pprint(vars(smarthome_data), depth=3)

            await asyncio.sleep(10)

asyncio.run(main())