import os

from . import config

config.load()

def create_token():
	if config.config.get(config.TOKEN) is None:

		print("No token exists!")
		
		token = input("Enter Token: ")
		config.config[config.TOKEN] = token

		config.save()


create_token()


from . import bot


def serve():
	print("Starting Bot..")
	bot.start()
