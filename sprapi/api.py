import aiohttp

from sprapi.classes import Information


class SPRadioApi:
    __api_url = 'https://radio.spworlds.city/api'

    async def __request_get(self, path: str = None):
        session = aiohttp.ClientSession()

        async with session.get(self.__api_url + path) as response:
            result = await response.json()
            await session.close()
            return result

    async def get_information(self) -> Information:
        res = await self.__request_get("/nowplaying/1")
        return Information(res)

    async def get_now_playing(self):
        info = await self.get_information()
        return info.now_playing
