import json
import asyncio
import websockets
from websockets.http import Headers
import pprint

from .console import console
from .settings import get_settings
import pkg_resources


class WebsocketClient(object):
    def __init__(self, host: str, token: str, proto: str, api_version: str = "v3.0"):
        self.host = host
        self.proto = proto
        self.api_version = api_version
        self.websocket = None
        self.do_listen = True
        self.token = token
        self.queue = asyncio.Queue()
        self._connected = False

    @property
    def user_agent(self):
        return {
            "user-agent":
                f"threedi-ws-client/{pkg_resources.get_distribution('threedi_ws_client').version}"
        }

    def get_queue(self):
        return self.queue

    async def is_connected(self):
        while self._connected is False:
            await asyncio.sleep(0.5)

    async def listen(self, endpoint_uri: str):
        uri = f"{self.proto}://{self.host}/{self.api_version}/{endpoint_uri}"
        console.print(f"Trying to connect to {uri} now...")
        headers = Headers(authorization=f"{self.token}")
        headers.update(**self.user_agent)
        sim_time: Optional[int] = None
        async with websockets.connect(uri, extra_headers=headers) as websocket:
            console.print(f"Connected to {uri}")
            self._connected = True
            async for message in websocket:
                try:
                    message = json.loads(message)
                    content = message["data"]
                    try:
                        sim_time = content["time"]
                    except (KeyError, TypeError):
                        pass
                    if sim_time is not None:
                        message["sim_time"] = sim_time
                    await self.queue.put(message)
                except websockets.exceptions.ConnectionClosedOK:
                    self.do_listen = False
        console.print("Websocket connection closed")

    async def close(self):
        self.do_listen = False
        if self.websocket:
            await self.websocket.close()
