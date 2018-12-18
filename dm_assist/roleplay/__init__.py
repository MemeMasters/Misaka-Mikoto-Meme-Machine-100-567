import asyncio
import math
from discord.ext import commands

from dm_assist.config import config
from dm_assist import util

# Roleplay init module
class Roleplay:

    def __init__(self, bot):
        self.bot = bot
    
    async def print_dice(self, dice):
        # This is my job security
        dice_string = ',\n'.join(
            [', '.join(
                ["{}/{}".format(x[0], x[1])
                    for x in dice[i*10:i*10+9]
                ]) 
                for i in range(min(int(math.ceil(len(dice) / 10.0)), 4))
            ])

        await self.bot.say("Rolled:\n```\n{}{}\n```".format(dice_string, '...' if len(dice) > 30 else ''))

    @commands.command()
    async def calc(self, *, equation: str):
        """
        Calculates an equation.

        You can use other commands such as <times>d<sides>, adv(sides, times),
        dis(sides, times), top(sides, times, top_num_dice), bot(sides, times, bot_num_dice)
        """
        try:
            util.dice.logging_enabled = True
            value = util.calculator.parse_equation(equation)
            util.dice.logging_enabled = False
        except util.BadEquation as exception:
            await self.bot.say("{} Tell me again, but slower..".format(exception))
            return
        
        dice = util.dice.rolled_dice
        if len(dice) > 0:
            await self.print_dice(dice)

        await self.bot.say("According to my notes, the answer is: **{}**".format(value))

        if util.dice.low:
            asyncio.ensure_future(util.dice.load_random_buffer())


    @commands.command()
    async def roll(self, roll: str):
        '''Rolls X dice with Y sides. Usage: !roll XdY + 5..'''


        try:
            roll = roll.lower().split("d")

            util.dice.logging_enabled = True
            data = util.dice.roll_sum(int(roll[1]), int(roll[0]))
            util.dice.logging_enabled = False
        except IndexError:
            await self.bot.say("I can't understand what you're trying to say, the format is `<times>d<sides>`")
            return
        except ValueError:
            await self.bot.say("You're suppost to use numbers!")
            return

        dice = util.dice.rolled_dice
        if len(dice) > 1:
            await self.print_dice(dice)

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
        Rolls a die with disadvantage. Usage: dis [sides=20]
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
    
    @commands.command()
    async def top(self, times='4', sides='6', top_dice='3'):
        """
        Rolls a number of dice, and takes only the top dice.  Usage: top [times=4] [sides=6] [num_top_dice=3]
        """

        try:
            sides = int(sides)
            times = int(times)
            top_dice = int(top_dice)
        except ValueError:
            self.bot.say("You're supposed to enter number not whatever that was")

        util.dice.logging_enabled = True
        sum = util.dice.roll_top(sides, top_dice, times)
        util.dice.logging_enabled = False

        dice = util.dice.rolled_dice
        if len(dice) > 1:
            await self.print_dice(dice)
        
        await self.bot.say("You got **{}**".format(sum))
        
        if util.dice.low:
            asyncio.ensure_future(util.dice.load_random_buffer())
    
    @commands.command(name='bot')
    async def bottom(self, times='4', sides='6', top_dice='3'):
        """
        Rolls a number of dice, and takes only the bottom dice.  Usage: bot [times=4] [sides=6] [num_top_dice=3]
        """

        try:
            sides = int(sides)
            times = int(times)
            top_dice = int(top_dice)
        except ValueError:
            self.bot.say("You're supposed to enter number not whatever that was")

        util.dice.logging_enabled = True
        sum = util.dice.roll_top(sides, top_dice, times, False)
        util.dice.logging_enabled = False

        dice = util.dice.rolled_dice
        if len(dice) > 1:
            await self.print_dice(dice)
        
        await self.bot.say("You got **{}**".format(sum))
        
        if util.dice.low:
            asyncio.ensure_future(util.dice.load_random_buffer())
