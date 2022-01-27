import asyncio

import tanjun
import datetime
import aiohttp

from bot.injected.database_communicator import DatabaseCommunicator
from shared.config import AlairaConfig

component = tanjun.Component(name="test")


@component.with_command
@tanjun.as_message_command("dbping")
async def database_ping(ctx: tanjun.context.MessageContext,
                        config: AlairaConfig = tanjun.injected(type=AlairaConfig),
                        database_communicator: DatabaseCommunicator = tanjun.injected(type=DatabaseCommunicator)):
    for count in [1, 50, 500, 5000, 50000]:
        message = await ctx.respond("Pinging database...")
        start = datetime.datetime.now()
        for i in range(1, count):
            await database_communicator.send(op="ping")
        duration = datetime.datetime.now() - start
        await message.edit(f"Response time {duration.seconds}.{duration.microseconds // 1000:>0}s for {count} pings")


@tanjun.as_loader
def load_component(client: tanjun.Client) -> None:
    client.add_component(component.copy())
