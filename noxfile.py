import nox

TARGETS = ["bot/", "database/", "dashboard/", "utils.py/", "main.py"]


@nox.session
def lint(session):
    session.install("flake8")
    session.run("flake8", ".")


@nox.session
def black(session):
    session.install("black")
    session.run("black", *TARGETS)
