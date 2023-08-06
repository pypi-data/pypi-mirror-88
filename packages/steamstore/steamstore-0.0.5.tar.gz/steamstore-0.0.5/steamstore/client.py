import logging
import asyncio

import aiohttp


from .defaults import *
from .app import App
from .featured import FeaturedList

log = logging.getLogger(__name__)

class Client:
    """Main class for the Steam API"""

    def __init__(self, *, loop=None, **opts):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.ready = False
        self.http = None

    def __cleanup(self):
        loop = self.loop

        if self.http:
            asyncio.ensure_future(self.http.close(), loop=loop)

    def stop(self):
        self.__cleanup()

    def __build_api(self, path:str, qs:dict=None, **args):
        url = base_api + path

        if qs:
            url += "?" + '&'.join([name + "=" + str(value) for name, value in qs.items()])

        return url

    async def __get_json(self, req:aiohttp.client_reqrep.ClientResponse, *args, **kwargs) -> dict:
        json_resp = None
        try:
            json_resp = await req.json()
        except:
            print("Error")
            return # TODO: Handle this

        return json_resp

    

    async def start(self, *args, **kwargs):
        
        self.http = await aiohttp.ClientSession().__aenter__()
        self.ready = True

    def run(self, *args, **kwargs):

        loop = self.loop

        async def runner():
            try:
                await self.start(*args, **kwargs)
            finally:
                pass # TODO: Handle this

        asyncio.ensure_future(runner(), loop=loop)
        
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            self.__cleanup()


    async def get_app_from_id(self, appid:int, currency_code:str="us", language_code:str="en"):

        req = await self.http.get(self.__build_api("appdetails", {"appids":appid, "cc":currency_code, "l":language_code}))
        json_resp = await self.__get_json(req)
        for item in json_resp:
            data = json_resp[item]
            return App(data=data["data"]) if data["success"] else None # TODO: Handle This

    async def get_featured(self, *args, **kwargs):

        req = await self.http.get(self.__build_api("featured"))
        json_resp = await self.__get_json(req)
        return FeaturedList(data=json_resp)
