import typing

from sqlalchemy import select
from sqlalchemy.engine import Engine, Row
from sqlalchemy.orm import sessionmaker

import database.tables as tb

prefixes: dict[int, str] = {}


def get_prefix(op: str, engine: Engine, session_maker: sessionmaker, **data):
    guild_id: int = data["guild"]
    try:
        return prefixes[guild_id]
    except KeyError:
        with session_maker.begin() as session:
            row: typing.Optional[tb.GuildConfigs] = session.query(tb.GuildConfigs).filter_by(guild=guild_id).first()
            if not row:
                session.add(tb.GuildConfigs(guild=guild_id))
                prefixes[guild_id] = "!"
                return {"prefix": "!", "status": 200}
            prefixes[guild_id] = row.prefix
            return {"prefix": row.prefix, "status": 200}


def set_prefix(op: str, engine: Engine, session_maker: sessionmaker, **data):
    guild_id: int = data["guild"]
    with session_maker.begin() as session:
        session.query(tb.GuildConfigs).filter_by(guild=guild_id).update({"prefix": data["prefix"]})
        prefixes[guild_id] = data["prefix"]
        return {"status": 200}


def setup(routes):
    routes["get prefix"] = get_prefix
    routes["set prefix"] = set_prefix
