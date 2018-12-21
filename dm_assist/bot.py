import discord
from discord.ext import commands

from . import config
from .config import config as conf

from . import voice
from . import misc
from . import roleplay

class Bot:

    def __init__(self):
        self.bot = None
    
    def setup(self):
        self.bot = commands.Bot(
            command_prefix=commands.when_mentioned_or(conf.config.prefix),
            description='An attempt to understand the confusing world around me.'
        )
            
        self.bot.add_cog(voice.Music(self.bot))
        self.bot.add_cog(misc.Misc(self.bot))
        self.bot.add_cog(roleplay.Roleplay(self.bot))


    def run(self):
        if self.bot is None:
            self.setup()

        if not discord.opus.is_loaded():
            # the 'opus' library here is opus.dll on windows
            # or libopus.so on linux in the current directory
            # you should replace this with the location the
            # opus library is located in and with the proper filename.
            # note that on windows this DLL is automatically provided for you
            try:
                discord.opus.load_opus(conf.config.voice.opus)
            except discord.opus.OpusError as e:
                print(e)
                print("Unable to load 'opus' library")

                print("voice cannot be used until opus is configured.")
                print("Set the path to libopus.so in 'config / voice / opus' in config.yaml")

        self.bot.run(conf.config.token)
    
    def stop(self):
        if self.bot is None:
            return
        self.bot.logout()
        self.bot.close()
