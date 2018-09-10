import os

from . import config


def create_token():
	config.token_file
	if not os.path.exists(config.token_file):
		try:
			from secrets import token_hex
		except ImportError:
			from os import urandom

			def token_hex(nbytes=None):
				return urandom(nbytes).hex()

		print("No token file exists!")
		print("generating token..")

		token_file = open(config.token_file, 'w')
		token_file.write(token_hex(16))
		token_file.close()

create_token()


from . import bot


def start():
	print("Starting Bot..")
	bot.bot.start(bot.Token)
