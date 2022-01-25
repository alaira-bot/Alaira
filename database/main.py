import importlib
import json
import logging
import typing
from pathlib import Path

import simple_websocket.ws
from flask import Flask
import time

from flask_sock import Sock

from shared.config import AlairaConfigLoader

app = Flask("alaira-database")
config = AlairaConfigLoader.get_current()
sock = Sock(app)
route_callbacks: dict[str, typing.Callable[[str, dict], typing.Any]] = {}


@sock.route("/socket")
def main_socket(ws: simple_websocket.ws.Server):
    while True:
        data = json.loads(ws.receive())
        data_id = data.pop("id")
        data_op = data.pop("op")
        try:
            resp = {
                "id": data_id,
                **(route_callbacks[data_op](data_op, **data))
            }
            if "status" not in resp:
                logging.warning(f"Opcode {data_op} with data {data} did not return a status")
            ws.send(json.dumps(resp))
        except KeyError:
            logging.warning(f"Found unrecognized opcode {data_op}. Ignoring")
            ws.send(json.dumps({
                "id": data_id,
                "status": 500
            }))


@app.route("/kill")
def kill_route():
    print("Killing database")
    time.sleep(5)  # TODO
    print("Database killed")
    return "", 204


def load_route(path: str):
    module = importlib.import_module(path)
    module.setup(route_callbacks)


def run():  # started from the main file - not invoked manually
    for path in Path("database/routes").glob("**/*.py"):
        load_route(str(path).replace("/", ".")[:-3])
    app.run(port=config.database.port)
