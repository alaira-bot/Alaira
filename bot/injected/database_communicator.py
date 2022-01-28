import asyncio
import typing

import websockets

from shared.config import AlairaConfig
from asyncio import Queue
import json


class DatabaseCommunicator:
    def __init__(self, config: AlairaConfig):
        self._config = config
        self._queue = Queue()
        self._socket: websockets.client.WebSocketClientProtocol = None
        self._id = 0
        self._id_lock = asyncio.Lock()
        self._events: dict[int, asyncio.Event] = {}
        self._waiting: dict[int, dict] = {}
        self._prefix_cache: dict[int, str] = {}

    async def get_prefix_for(self, guild: int) -> str:
        try:
            return self._prefix_cache[guild]
        except KeyError:
            resp = await self.send("get prefix", guild=guild)
            if resp["status"] == 404:
                self._prefix_cache[guild] = "!"
                return "!"
            self._prefix_cache[guild] = (prefix := resp["prefix"])
            return prefix

    async def set_prefix_for(self, guild: int, prefix: str):
        await self.send("set prefix", guild=guild, prefix=prefix)
        self._prefix_cache[guild] = prefix

    @property
    def queue_size(self) -> int:
        return len(self._events)

    async def connect(self):
        self._socket = await websockets.connect(
            f"ws://127.0.0.1:{self._config.database.port}/socket"
        )
        asyncio.create_task(self.loop())

    async def loop(self):
        while True:
            message = json.loads(await self._socket.recv())
            message_id = message.pop("id")
            self._waiting[message_id] = message
            self._events[message_id].set()

    async def send(self, op: str, **params) -> dict:
        async with self._id_lock:
            id_waiting_for = self._id
            self._id += 1
        self._events[id_waiting_for] = asyncio.Event()
        self._events[id_waiting_for].clear()
        await self._socket.send(json.dumps({"id": id_waiting_for, "op": op, **params}))
        await self._events[id_waiting_for].wait()
        response = self._waiting.pop(id_waiting_for)
        del self._events[id_waiting_for]
        return response
