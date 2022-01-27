import typing
from pathlib import Path

import tanjun
import hikari

from bot.injected.database_communicator import DatabaseCommunicator
from shared.config import AlairaConfigLoader, AlairaConfig

config = AlairaConfigLoader.load("config.yaml")
client = hikari.GatewayBot(token=config.bot.token)
database_communicator = DatabaseCommunicator(config)


async def prefix_getter(ctx: tanjun.abc.MessageContext) -> typing.Iterable[str]:
    return [
        f"<@{client.get_me().id}>",
        f"<@!{client.get_me().id}>",
        await database_communicator.get_prefix_for(ctx.guild_id)
    ]


bot = (tanjun.Client
       .from_gateway_bot(client)
       .load_modules(*Path("./bot/modules").glob("**/*.py"))
       .set_prefix_getter(prefix_getter)
       .set_type_dependency(AlairaConfig, config)
       .set_type_dependency(DatabaseCommunicator, database_communicator))


@client.listen(hikari.StartedEvent)
async def on_ready(_):
    await database_communicator.connect()


def run():  # started from the main file - not invoked manually
    client.run()
