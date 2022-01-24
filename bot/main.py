import asyncio
import tanjun
import hikari

client = hikari.GatewayBot(token="")
bot = tanjun.Client.from_gateway_bot(client)


def run():  # started from the main file - not invoked manually
    client.run()
