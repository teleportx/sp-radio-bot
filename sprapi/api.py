import aiohttp

from sprapi.classes import Song, Information


class SPRadioApi:
    __api_url = 'https://radio.uuuuuno.net/api'

    async def __request_get(self, path: str = None):
        session = aiohttp.ClientSession()

        response = await session.get(self.__api_url + path)

        await session.close()
        return response

    async def get_information(self) -> Information:
        res = await self.__request_get("/nowplaying/1")
        json = await res.json()
        return Information(json)

    async def get_now_playing(self):
        info = await self.get_information()
        return info.now_playing
