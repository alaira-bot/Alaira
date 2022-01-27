import logging
import os
import sys

import rich.traceback

import utils.logger

rich.traceback.install()
logging.setLoggerClass(utils.logger.LoggingHandler)
logging.basicConfig(level=5)
logging.addLevelName(5, "TRACE")

loggers = {
    "socket": logging.CRITICAL,
    "main": logging.ERROR,
    "database": logging.WARNING,
    "hikari.bot": logging.INFO,
    "hikari.gateway": logging.DEBUG,
    "discord.http": 5
}
for k, v in loggers.items():
    logging.getLogger(k).log(v, "test")

logging.getLogger(__name__).info("multiline\ntest")
utils.logger.lprint("CUSTOM", "source", "Boop", source_style="bright_red bold",
                    message_style="bright_red italic underline on WHITE",
                    line_type_style="bold color(118)")

print(1/0)