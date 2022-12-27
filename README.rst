==================
 aio-watts-vision
==================

Status
======

.. image:: https://secure.travis-ci.org/mjkl-gh/aio-watts-vision.png?branch=master
   :target: http://travis-ci.org/mjkl-gh/aio-watts-vision
.. image:: https://coveralls.io/repos/mjkl-gh/aio-watts-vision/badge.png?branch=master
   :target: https://coveralls.io/r/mjkl-gh/aio-watts-vision?branch=master
.. image:: https://img.shields.io/pypi/v/aio-watts-vision.svg
   :target: https://pypi.python.org/pypi/aio-watts-vision
.. image:: https://readthedocs.org/projects/aio-watts-vision/badge/?version=latest
   :target: https://readthedocs.org/projects/aio-watts-vision/?badge=latest
   :alt: Documentation Status


Requirements
============

* Python 3.9 over

Features
========

* ToDo: Rewrite me.

Setup
=====

::

  $ python -m pip install --user aio-watts-vision
  or
  (venv)$ python -m pip install aio-watts-vision

Usage
=====

::

from aio_watts_vision.token_manager import TokenManager
from aio_watts_vision.auth import Auth
from aio_watts_vision.models.enums import Mode
from aio_watts_vision.models.smarthome import Smarthome
from aio_watts_vision.watts_vision_api import WattsVisionAPI

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
  >>>

