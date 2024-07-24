from modules.bot import Bot


params = ["../settings/config.json", "../settings/wot_bot.log"]

bot = Bot(*params)
bot.check_gift_status()
bot.config_props()
bot.get_gift()
bot.release_resources()
