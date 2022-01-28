import importlib
import json
import logging
import typing
from pathlib import Path

import simple_websocket.ws
from flask import Flask
import time

from flask_sock import Sock
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from shared.config import AlairaConfigLoader
from sqlalchemy import create_engine
from database.tables import setup

app = Flask("alaira-database")
config = AlairaConfigLoader.get_current()
sock = Sock(app)
db_engine = create_engine("sqlite+pysqlite:///database.db")
session_maker = sessionmaker(db_engine)
route_callbacks: dict[
    str, typing.Callable[[str, Engine, sessionmaker, dict], typing.Any]
] = {}

db_engine.connect()
setup(db_engine)

logger = logging.getLogger("database")


@sock.route("/socket")
def main_socket(ws: simple_websocket.ws.Server):
    logging.getLogger("socket").info("Database websocket connected")
    while True:
        data = json.loads(ws.receive())
        data_id = data.pop("id")
        data_op = data.pop("op")
        try:
            resp = {
                "id": data_id,
                **(route_callbacks[data_op](data_op, db_engine, session_maker, **data)),
            }
            if "status" not in resp:
                logging.warning(
                    f"Opcode {data_op} with data {data} did not return a status."
                )
            ws.send(json.dumps(resp))
        except KeyError:
            logging.warning(f"Found unrecognized opcode {data_op}. Ignoring.")
            ws.send(json.dumps({"id": data_id, "status": 500}))


@app.route("/kill")
def kill_route():
    logger.info("Killing database")
    time.sleep(5)  # TODO
    logger.info("Database killed")
    return "", 204


def load_route(path: str):
    module = importlib.import_module(path)
    module.setup(route_callbacks)


def run():  # started from the main file - not invoked manually
    for path in Path("database/routes").glob("**/*.py"):
        route_name = str(path).replace("/", ".")[:-3]
        logger.info(f"Loading {route_name}")
        load_route(route_name)
    logger.info("Starting flask app")
    app.run(port=config.database.port)
