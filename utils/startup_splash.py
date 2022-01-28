from textwrap import dedent

import alembic
import rich as r
import hikari
import sqlalchemy
import tanjun
import sys
from rich.panel import Panel

panel = Panel(
    f"""
Python        {sys.version}\n
Hikari        {hikari.__version__}
Tanjun        {tanjun.__version__}\n
SQLAlchemy    {sqlalchemy.__version__}
Alembic       {alembic.__version__}
""",
    title="[bold bright_white]Aliara Bot[/bold bright_white]   [white]System Details[/white]",
)

r.print(panel)
