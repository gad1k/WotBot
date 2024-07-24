from wot_bot import WotBot


bot = WotBot("../settings/config.json", "../settings/wot_bot.log")
bot.check_gift_status()
bot.config_props()
bot.get_gift()
bot.release_resources()