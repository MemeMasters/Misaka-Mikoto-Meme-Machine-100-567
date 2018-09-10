from . import bot

# __init__.py is the main file for the package.

def start():
	print("Starting Bot..")
	bot.bot.start(bot.Token)
