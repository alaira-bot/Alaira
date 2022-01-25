import multiprocessing
import bot.main as bot
import dashboard.main as dashboard
import database.main as database
import utils.config as cfg
import requests
import logging

from shared.config import AlairaConfigLoader

cfg.validate("config.yaml", "schema/config_schema.yaml")
logging.basicConfig(level=logging.INFO)
logging.getLogger("py.warnings").setLevel(logging.ERROR)

bot_proc = multiprocessing.Process(target=bot.run)
dashboard_proc = multiprocessing.Process(target=dashboard.run)
database_proc = multiprocessing.Process(target=database.run)

bot_proc.start()
dashboard_proc.start()
database_proc.start()
bot_proc.join()

config = AlairaConfigLoader.load("config.yaml")
requests.get(f"http://127.0.0.1:{config.database.port}/kill")

dashboard_proc.kill()
database_proc.kill()

