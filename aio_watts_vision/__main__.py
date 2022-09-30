import asyncio
import aiohttp

from aio_watts_vision import Auth



async def main():
    async with aiohttp.ClientSession() as session:
        auth = Auth(session, "http://example.com/api", "secret_access_token")

        # This will fetch data from http://example.com/api/lights
        resp = await auth.request("get", "lights")
        print("HTTP response status code", resp.status)
        print("HTTP response JSON content", await resp.json())

if __name__ == "__main__":
    asyncio.run(main())