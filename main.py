import multiprocessing
import bot.main as bot
import dashboard.main as dashboard
import database.main as database
import utils.config as cfg

cfg.validate("config.yaml", "schema/config_schema.yaml")

bot_proc = multiprocessing.Process(target=bot.run)
dashboard_proc = multiprocessing.Process(target=dashboard.run)
database_proc = multiprocessing.Process(target=database.run)

bot_proc.start()
dashboard_proc.start()
database_proc.start()
bot_proc.join()