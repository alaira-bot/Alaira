import asyncio
import requests


class DatabaseCommunicator:
    def __init__(self, port: int):
        self._loop = asyncio.get_event_loop()
        self._port = port
        self._db_url = f"http://127.0.0.1:{port}"

    def kill(self):
        self._loop.run_in_executor(None, requests.get(f"{self._db_url}/kill"))

