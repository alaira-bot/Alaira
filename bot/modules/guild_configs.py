import hikari
import tanjun

from bot.injected.database_communicator import DatabaseCommunicator
from shared.config import AlairaConfig

component = tanjun.Component(name="guild_configs")


@component.with_command
@tanjun.with_author_permission_check(hikari.Permissions.ADMINISTRATOR)
@tanjun.with_argument("_prefix")
@tanjun.as_message_command("prefix")
async def prefix(ctx: tanjun.abc.MessageContext, _prefix: str,
                 config: AlairaConfig = tanjun.injected(type=AlairaConfig),
                 database_communicator: DatabaseCommunicator = tanjun.injected(type=DatabaseCommunicator)):
    await database_communicator.set_prefix_for(ctx.guild_id, _prefix)
    await ctx.respond(f"Prefix set to `{_prefix}`")


@tanjun.as_loader
def load_component(client: tanjun.Client) -> None:
    client.add_component(component.copy())
