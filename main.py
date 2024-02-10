from wot_bot import WotBot


bot = WotBot("config.json")
bot.check_logs()
bot.config_props()
bot.start_browser()
bot.get_gift()
bot.stop_browser()
