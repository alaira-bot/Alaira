from pathlib import Path

import tanjun
import hikari

from bot.injected.database_communicator import DatabaseCommunicator
from shared.config import AlairaConfigLoader, AlairaConfig

config = AlairaConfigLoader.load("config.yaml")
client = hikari.GatewayBot(token=config.bot.token)
database_communicator = DatabaseCommunicator(config)

bot = (tanjun.Client
       .from_gateway_bot(client)
       .load_modules(*Path("./bot/modules").glob("**/*.py"))
       .add_prefix("!")
       .set_type_dependency(AlairaConfig, config)
       .set_type_dependency(DatabaseCommunicator, database_communicator))


@client.listen(hikari.StartedEvent)
async def on_ready(_):
    await database_communicator.connect()


def run():  # started from the main file - not invoked manually
    client.run()
