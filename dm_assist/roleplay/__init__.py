from discord.ext import commands

from dm_assist.config import config
from dm_assist import util

# Roleplay init module
class Roleplay:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, dice: str):
        '''Rolls X dice with Y sides. Usage: !roll XdY XdY ..'''

        try:
            data = util.parse_die_roll(dice)
        except util.BadFormat as exception:
            await self.bot.say(exception)
            return

        total = data['total']

        # + " with " + str(TotalCrits) + " crits!")
        if data['rolls'] is 1:
            await self.bot.say(str(total))
            
            if data['sides'][0] is 1:
                await self.bot.say(util.get_random_line(config.lines.dumb))
            elif data['crits'] is 1:
                await self.bot.say(util.get_random_line(config.lines.crits))
            elif data['fails'] is 1:
                await self.bot.say(util.get_random_line(config.lines.critFails))
        else:
            message = str(total)
            
            if data['sides'][0] is 1:
                await self.bot.say(message)
                await self.bot.say(util.get_random_line(config.lines.dumb))
            else:
                if data['crits'] > 0:
                    message += " with {} crits".format(data['crits'])

                if data['fails'] > 0:
                    message += "{} {} fails".format(
                        " with" if data['crits'] is 0 else ", and",
                        data['fails'])
                await self.bot.say(message)

        for key, val in config['lines']['on_roll'].items():
            if str(total) == key:
                await self.bot.say(util.get_random_line(val))
                break

    @commands.command(pass_context=True) #coinflip stuff
    async def coinflip(self, ctx):
        '''Flips a coin.'''
        HeadTails, _, _ = util.roll(1, 2)
        if HeadTails == 1:
            await  self.bot.say("Tails, but you're dead either way")
        else:
            await  self.bot.say("Heads, but you're dead either way")