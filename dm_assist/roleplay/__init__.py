import asyncio
from discord.ext import commands

from dm_assist.config import config
from dm_assist import util

# Roleplay init module
class Roleplay:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def calc(self, *, equation: str):
        """
        Calculates an equation.

        You can use other commands such as <times>d<sides>, adv(sides, times),
        dis(sides, times), top(sides, times, top_num_dice), bot(sides, times, bot_num_dice)
        """

        try:
            value = util.calculator.parse_equation(equation)
        except util.BadEquation as exception:
            await self.bot.say("{} Tell me again, but slower..".format(exception))
            return
        
        await self.bot.say("According to my notes, the answer is: **{}**".format(value))

        if util.dice.low:
            asyncio.ensure_future(util.dice.load_random_buffer())


    @commands.command()
    async def roll(self, roll: str):
        '''Rolls X dice with Y sides. Usage: !roll XdY + 5..'''


        try:
            roll = roll.lower().split("d")
            data = util.dice.roll_sum(int(roll[1]), int(roll[0]))
        except IndexError:
            await self.bot.say("I can't understand what you're trying to say, the format is `<times>d<sides>`")
            return
        except ValueError:
            await self.bot.say("You're suppost to use numbers!")
            return

        total = data[0]
        rolls = roll[0]
        sides = roll[1]

        # + " with " + str(TotalCrits) + " crits!")
        if rolls is 1:
            await self.bot.say(str(total))
            
            if sides is 1:
                await self.bot.say(util.get_random_line(config.lines.dumb))
            elif data[1] is 1:
                await self.bot.say(util.get_random_line(config.lines.crits))
            elif data[2] is 1:
                await self.bot.say(util.get_random_line(config.lines.critFails))
        else:
            message = str(total)
            
            if sides is 1:
                await self.bot.say(message)
                await self.bot.say(util.get_random_line(config.lines.dumb))
            else:
                if data[1] > 0:
                    message += " with {} crits".format(data[1])

                if data[2] > 0:
                    message += "{} {} fails".format(
                        " with" if data[1] is 0 else ", and",
                        data[2])
                await self.bot.say(message)

        for key, val in config['lines']['on_roll'].items():
            if str(total) == key:
                await self.bot.say(util.get_random_line(val))
                break
        
        if util.dice.low:
            asyncio.ensure_future(util.dice.load_random_buffer())

    @commands.command() #coinflip stuff
    async def coinflip(self):
        '''Flips a coin.'''
        HeadTails = util.dice.roll(2)

        if HeadTails == 1:
            await  self.bot.say("Tails, but you're dead either way")
        else:
            await  self.bot.say("Heads, but you're dead either way")

        if util.dice.low:
            asyncio.ensure_future(util.dice.load_random_buffer())
        
    
    @commands.command()
    async def adv(self, sides='20'):
        """
        Rolls a die with advantage. Usage: adv [sides]
        """
        try:
            sides = int(sides)
        except ValueError:
            self.bot.say("That's not a number, silly.")
            return

        d1 = util.dice.roll(sides)
        d2 = util.dice.roll(sides)

        final = max(d1, d2)

        await self.bot.say("You rolled a {}, and a {}.\n you got a **{}**.".format(d1, d2, final))
        if d1 is d2:
            await self.bot.say("You're dead either way :)")
    
        if util.dice.low:
            asyncio.ensure_future(util.dice.load_random_buffer())

    @commands.command()
    async def dis(self, sides='20'):
        """
        Rolls a die with disadvantage. Usage: dis [sides]
        """
        try:
            sides = int(sides)
        except ValueError:
            self.bot.say("That's not a number, silly.")
            return

        d1 = util.dice.roll(sides)
        d2 = util.dice.roll(sides)

        final = min(d1, d2)

        await self.bot.say("You rolled a {}, and a {}.\n you got a **{}**.".format(d1, d2, final))
        if d1 is d2:
            await self.bot.say("You're dead either way :)")

        if util.dice.low:
            asyncio.ensure_future(util.dice.load_random_buffer())