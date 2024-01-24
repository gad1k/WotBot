from wot_bot import WotBot


bot = WotBot("config.json")
bot.config_props()
bot.start_browser(False)
bot.get_gift()
bot.stop_browser()
