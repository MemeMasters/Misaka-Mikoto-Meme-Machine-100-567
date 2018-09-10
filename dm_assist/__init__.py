import os
import discord
from discord.ext import commands

from dm_assist import config
from dm_assist.config import config as conf


Bot = commands.Bot(
	command_prefix=commands.when_mentioned_or(conf['config']['prefix']),
	description='An attempt to understand the confusing world around me.'
)

from dm_assist import voice
Bot.add_cog(voice.Music(Bot))


# Prevent circular imports
from dm_assist import bot

def create_token():
	if config.config['config'].get('token') is None:

		print("No token exists!")
		
		token = input("Enter Token: ")
		config.config['config']['token'] = token

		config.save()


def serve():
	create_token()

	print("Starting Bot..")

	bot.start(config.config['config']['token'])
