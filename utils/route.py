import typing

import aiohttp


class Route:
    def __init__(self, method: typing.Literal["GET", "POST"],
                 base: str, port: int, path: str, /, *, data: typing.Optional[typing.Any] = None,
                 json: typing.Optional[typing.Any] = None):
        self._url = f"http://{base}:{port}/{path}"
        self._data = data
        self._method = method
        self._json = json

    async def run(self):
        return await aiohttp.request(self._method, self._url, data=self._data, json=self._json)


class RouteGenerator:
    def __init__(self, url: str, port: int):
        self._url = url
        self._port = port

    def get(self, path: str, data: typing.Optional[typing.Any] = None,
            json: typing.Optional[typing.Any] = None):
        return Route("GET", self._url, self._port, path, data=data, json=json)

    def get(self, path: str, data: typing.Optional[typing.Any] = None,
            json: typing.Optional[typing.Any] = None):
        return Route("POST", self._url, self._port, path, data=data, json=json)
