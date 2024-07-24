from modules.wot_bot import WotBot


params = ["../settings/config.json", "../settings/wot_bot.log"]

bot = WotBot(*params)
bot.check_gift_status()
bot.config_props()
bot.get_gift()
bot.release_resources()
