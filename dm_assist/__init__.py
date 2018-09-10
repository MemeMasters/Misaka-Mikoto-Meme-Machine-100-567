import os

from dm_assist import config, bot

config.load()

def create_token():
	if config.config.get(config.TOKEN) is None:

		print("No token exists!")
		
		token = input("Enter Token: ")
		config.config[config.TOKEN] = token

		config.save()


def serve():
	create_token()

	print("Starting Bot..")

	bot.start(config.config[config.TOKEN])
