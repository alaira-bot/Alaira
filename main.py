import logging
import multiprocessing
import time
from rich.traceback import install as rich_install
import utils.config as cfg
import utils.logger
import requests
from shared.config import AlairaConfigLoader
import signal

logging.setLoggerClass(utils.logger.LoggingHandler)
import bot.main as bot  # noqa E402
import database.main as database  # noqa E402
# import dashboard.main as dashboard

rich_install(show_locals=True)

logger = logging.getLogger("main")
cfg.validate("config.yaml", "schema/config_schema.yaml")
logging.basicConfig(level=logging.INFO)
logging.getLogger("py.warnings").setLevel(logging.ERROR)

bot_proc = multiprocessing.Process(target=bot.run)
# dashboard_proc = multiprocessing.Process(target=dashboard.run)
database_proc = multiprocessing.Process(target=database.run)
config = AlairaConfigLoader.load("config.yaml")
logger.info("Starting database process")
database_proc.start()

logger.info("Pinging database")
for i in range(1, 10):
    try:
        requests.get(f"http://127.0.0.1:{config.database.port}/ping")
        break
    except (ConnectionRefusedError, requests.exceptions.ConnectionError):
        logger.warning("Connection refused... trying again in 1 second")
        time.sleep(1)
else:
    logger.critical("Database process not started... exiting")
    exit(-1)

# dashboard_proc.start()
logger.info("Starting bot process")
bot_proc.start()
signal.signal(signal.SIGINT, lambda sig, frame: bot_proc.kill())
logger.info("Joining bot process")
bot_proc.join()
logger.info("Bot process stopped")

logger.info("Killing database")
try:
    requests.get(f"http://127.0.0.1:{config.database.port}/kill")
    logger.info("Database kill signal sent")
except (ConnectionRefusedError, requests.exceptions.ConnectionError):
    logger.critical("Database /kill endpoint refused to connect.. Data may have been lost")
# dashboard_proc.kill()
database_proc.kill()
logger.info("Database process killed")
