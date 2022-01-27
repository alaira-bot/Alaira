# TODO remove
def ping(op: str, engine, session_maker, **data):
    return {"status": 204}


def setup(routes):
    routes["ping"] = ping
