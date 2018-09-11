import os
from contextlib import contextmanager
import signal

import discord
from discord.ext import commands

from dm_assist.config import config

from dm_assist import voice
from dm_assist import misc
from dm_assist import roleplay


Bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(config['config']['prefix']),
    description='An attempt to understand the confusing world around me.'
)


Bot.add_cog(voice.Music(Bot))
Bot.add_cog(roleplay.RolePlay(Bot))
Bot.add_cog(misc.Misc(Bot))


if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    try:
        discord.opus.load_opus(config['config']['voice']['opus'])
    except discord.opus.OpusError as e:
        print(e)
        print("Unable to load 'opus' library")

        print("voice cannot be used until opus is configured.")
        print("Set the path to libopus.so in 'config / voice / opus' in config.yaml")


@Bot.event
async def on_ready():
    print("Hello Nerds")
    print("Name: {}".format(Bot.user.name))
    print("ID: {}".format(Bot.user.id))
    print("___________________________")
    #MainChannel = client.get_channel(MainChannelID)
    #await client.send_message(MainChannel, StartupLines[random.randint(0, len(StartupLines)-1 )])


def create_token():
    if config['config'].get('token') is None:

        print("No token exists!")
        
        token = input("Enter Token: ")
        config['config']['token'] = token

        config.save()


@contextmanager
def sigint_shutdown():

    original_sigint_handler = signal.getsignal(signal.SIGINT)

    def on_shutdown_req():
        print("Shutting down Bot..")
        Bot.logout()
        Bot.close()
        raise SystemExit

    signal.signal(signal.SIGINT, lambda sig, frame: on_shutdown_req())

    try:
        print("Press Ctrl-C to stop the Bot")
        yield
    except Exception:
        raise
    finally:
        signal.signal(signal.SIGINT, original_sigint_handler)

def serve():
    create_token()

    print("Starting Bot..")
    
    with sigint_shutdown():
        Bot.run(config['config']['token'])
