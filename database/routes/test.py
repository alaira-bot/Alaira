# TODO remove
def ping(op: str, **data):
    return {"status": 204}


def setup(routes):
    routes["ping"] = ping
