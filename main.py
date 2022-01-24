import multiprocessing
import bot.main as bot
import dashboard.main as dashboard
import database.main as database
from database.communicator import DatabaseCommunicator
import utils.config as cfg

cfg.validate("config.yaml", "schema/config_schema.yaml")

bot_proc = multiprocessing.Process(target=bot.run)
dashboard_proc = multiprocessing.Process(target=dashboard.run)
database_proc = multiprocessing.Process(target=database.run)
database_communicator = DatabaseCommunicator(5000)

bot_proc.start()
dashboard_proc.start()
database_proc.start()
bot_proc.join()
database_communicator.kill()
dashboard_proc.kill()
database_proc.kill()