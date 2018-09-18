import os
import json

from discord.ext import commands

from dm_assist.config import config
from dm_assist import util

from dm_assist import sql
from dm_assist.sql.roleplay_model import Character as Character_model, User as User_model


class NoUserError(Exception):
    pass


class Character:

    def __init__(self, bot):
        self.bot = bot

    async def get_user(self, session, id):
        user = session.query(User_model).get(id)
        if user is None:
            await self.bot.say("You do not have any characters!  Create one first!")
        return user

    @staticmethod
    def get_user_name(args):
        return ' '.join(args).lower()
    
    @staticmethod
    def get_user_id(ctx):
        return ctx.message.author.id
    
    @staticmethod
    def length(prefix, value, width):
            total_length = len(prefix) + len(value)

            return prefix + " " * (width - total_length) + value

    def get_stats(self, character: Character_model):
        stats = self.__class__.length("Strength:", str(character.strength), 20) + '\n' + \
                self.__class__.length("Intelligence:", str(character.intelligence), 20) + '\n' + \
                self.__class__.length("Wisdom:", str(character.wisdom), 20) + '\n' + \
                self.__class__.length("Dexterity:", str(character.dexterity), 20) + '\n' + \
                self.__class__.length("Constitution:", str(character.constitution), 20) + '\n' + \
                self.__class__.length("Charisma:", str(character.charisma), 20) + '\n' + \
                self.__class__.length("Comeliness:", str(character.comeliness), 20) + '\n'

        return stats

    async def get_character(self, session, name, user_id) -> (Character_model, User_model):
        user = session.query(User_model).get(user_id)
        if user is None:
            await self.bot.say(util.get_random_line(config.lines.user_error.no_user))
            raise NoUserError()

        try:
            char = user.get_character(name=name)

            if char is None:
                if name is None:
                    await self.bot.say(util.get_random_line(config.lines.user_error.no_char))
                else:
                    await self.bot.say(util.get_random_line(config.lines.user_error.wrong_char))
                raise NoUserError()
        except sql.roleplay_model.TooManyCharactersError:
            await self.bot.say(util.get_random_line(config.lines.user_error.too_many_char))
            raise NoUserError()
        
        return char, user
        
    @commands.command(pass_context=True)
    async def rollstats(self, ctx, *args):
            '''Rolls 7 sets of 3d6, with mild flexibility. 
            Increasing the number of dice per stat will not create huge numbers, as the stats are generated from the highest three numbers rolled per set. 
            Usage: !stats [x] [y], where x is the number of dice per stat and y is the number of stats. 
            If you have made a character with !newchar, it will apply the stats rolled without confirmation unless your character already has stats.'''
            
            character = self.get_user_name(args)
            if character == '':
                character = None

            session = sql.sql.getSession()

            try:
                char, _ = await self.get_character(session, character, self.get_user_id(ctx))
            except NoUserError:
                return

            Strength, _, _ = util.roll(3, 6)
            Intelligence, _, _ = util.roll(3, 6)
            Wisdom, _, _ = util.roll(3, 6)
            Dexterity, _, _ = util.roll(3, 6)
            Constitution, _, _ = util.roll(3, 6)
            Charisma, _, _ = util.roll(3, 6)
            Comeliness, _, _ = util.roll(3, 6)

            char.strength = Strength
            char.intelligence = Intelligence
            char.wisdom = Wisdom
            char.dexterity = Dexterity
            char.constitution = Constitution
            char.charisma = Charisma
            char.comeliness = Comeliness

            session.commit()

            message = "Set the following stats to {}\n**```css\n{}\n```**".format(
                util.format_name(char.name),
                self.get_stats(char)
            )

            await self.bot.say(message)
    
    @commands.command(pass_context=True)
    async def setstat(self, ctx, *args):
        '''
        Set a specific stat value.
        Usage: !setStat [character] <str|int|wis|dex|con|cha|com> <value>
        '''

        # Load the arguments
        if len(args) is 2:
            character = None
        elif len(args) >= 3:
            character = Character.get_user_name(args[:-2])
        else:
            await self.bot.say("Usage: !setStat [character] <str|int|wis|dex|con|cha|com> <value>")
            return

        pre_stat = args[-2]
        value = args[-1]

        # make sure the stat is lowercase and only the first 3 characters
        stat = pre_stat.lower()[:3]
        val = 10

        # Parse the value
        try:
            val = int(value)
        except ValueError:
            await self.bot.say("{} is not a number".format(value))
            return

        session = sql.sql.getSession()
        try:
            char, _ = await self.get_character(session, character, self.get_user_id(ctx))
        except NoUserError:
            return

        # Set the stat
        if stat == 'str':
            char.strength = val
        elif stat == 'int':
            char.intelligence = val
        elif stat == 'wis':
            char.wisdom = val
        elif stat == 'dex':
            char.dexterity = val
        elif stat == 'con':
            char.constitution = val
        elif stat == 'cha':
            char.charisma = val
        elif stat == 'com':
            char.comeliness = val
        else:
            await self.bot.say("{} is not a valid stat".format(pre_stat))
            return
        
        session.commit()

        await self.bot.say("{}\nSuccessfully changed your {} stat to {}".format(
            util.get_random_line(config.lines.crits),
            stat, val
        ))

        print("Changed {}'s {} stat to be {}\n{}".format(char.id, stat, val, char))

    @commands.command(pass_context=True)
    async def newchar(self, ctx, *args):
        """This command creates a character unique to your Discord user id. Usage: !newchar <name>"""
        
        name = Character.get_user_name(args)

        if name == '':
            await self.bot.say("Usage: !newchar <Name>")
            return
        
        session = sql.sql.getSession()
        user_id = ctx.message.author.id

        # Check if the user is saved in the database
        user = session.query(User_model).get(user_id)
        if user is None:
            # Add the user to the database
            user = User_model(id=user_id)
            session.add(user)
            session.commit()

        # Check if there is already a character by that name that the user owns
        exist_characters = user.get_character(name=name)
        if exist_characters is not None:
            await self.bot.say("{} already exists! There is no need to recreate him.".format(util.format_name(name)))
            return

        new_character = Character_model(name=name)
        user.characters.append(new_character)
        session.commit()

        await self.bot.say("{}\nSuccessfully created a new character by the name of {}".format(
            util.get_random_line(config.lines.crits),
            util.format_name(name)
        ))

        print("Created new Character: {}\nThat belongs to {}".format(new_character, user))

    @commands.command(pass_context=True)
    async def setlevel(self, ctx, *args):
        '''Set the level of a character'''

        if len(args) is 1:
            character = None
        else:
            character = Character.get_user_name(args[:-1])

        try:
            level = int(args[-1])
            if level < 1:
                raise ValueError()
        except ValueError:
            await self.bot.say("{} is not a valid level".format(level))
            return
        
        session = sql.sql.getSession()

        try:
            char, _ = await self.get_character(session, character, self.get_user_id(ctx))
        except NoUserError:
            return

        classs = char.get_class()

        if classs is None:
            await self.bot.say("{} doesn't have a class yet.  You need to give them a class first".format(util.format_name(char.name)))
            return
        
        if classs.max_level is not -1 and level > classs.max_level:
            await self.bot.say("{}\n{}s have a max level of {}".format(util.get_random_line(config.lines.critFails), char.classname, classs.max_level))
            return
        
        old_xp = char.xp

        if level is classs.get_level(old_xp):
            await self.bot.say("{}\n{} is already at that level!".format(util.get_random_line(config.lines.dumb), util.format_name(char.name)))
            return

        char.xp = classs.get_xp(level) + 1

        session.commit()

        await self.bot.say("{} has received {:,} xp. and is now level {} ({})".format(
            util.format_name(char.name),
            char.xp - old_xp,
            level, classs.title[level - 1]
        ))

    @commands.command(pass_context=True)
    async def levelup(self, ctx, *args):
        '''Level up your character'''

        character = Character.get_user_name(args)
        character = None if character == '' else character

        session = sql.sql.getSession()
        
        try:
            char, _ = await self.get_character(session, character, self.get_user_id(ctx))
        except NoUserError:
            return

        classs = char.get_class()

        if classs is None:
            await self.bot.say("{} doesn't have a class yet.  You need to give them a class first".format(char.name))
            return
        
        old_xp = char.xp
        level = classs.get_level(old_xp)

        if level is classs.max_level:
            await self.bot.say("{} is already at their max level".format(char.name))
            return
        
        level += 1

        char.xp = classs.get_xp(level) + 1

        session.commit()

        await self.bot.say("{}\n{} has received {:,} xp and has leveled up to level {} ({})".format(
            util.get_random_line(config.lines.crits),
            util.format_name(char.name),
            char.xp - old_xp,
            level,
            classs.title[level - 1]
        ))

    @commands.command(pass_context=True)
    async def addxp(self, ctx, *args):
        '''Add xp to your character'''

        if len(args) is 1:
            character = None
        else:
            character = Character.get_user_name(args[:-1])

        xp = args[-1]

        try:
            xp = int(xp)

            if xp is 0:
                await self.bot.say(util.get_random_line(config.lines.dumb))
                return
        except ValueError:
            await self.bot.say("{} is not a number.  Try again.".format(args[-1]))
            return

        session = sql.sql.getSession()
        try:
            char, _ = await self.get_character(session, character, self.get_user_id(ctx))
        except NoUserError:
            return
        
        classs = char.get_class()
        
        if classs is None:
            await self.bot.say("{} doesn't have a class yet.  You need to give them a class first".format(char.name))
            return
        
        old_xp = char.xp
        if old_xp + xp < 0:
            await self.bot.say("You can't have a negative xp.")
            xp = -old_xp
        char.xp += xp

        session.commit()

        new_level = classs.get_level(char.xp)
        if new_level is not classs.get_level(old_xp):

            await self.bot.say("{} has received {:,} xp and has leveled {} to level {} ({})".format(
                util.format_name(char.name),
                xp,
                'up' if xp > 0 else 'down',
                new_level,
                classs.title[new_level - 1]
            ))
            return

        next_level = "\nOnly {:,} xp to next level".format(classs.xp[new_level - 1] - char.xp + 1)

        await self.bot.say("{} has received {:,} xp and now has {:,} xp{}".format(
            util.format_name(char.name),
            xp,
            char.xp,
            next_level if classs.max_level is not new_level else ""
        ))

    @commands.command(pass_context=True)
    async def setxp(self, ctx, *args):
        '''Set the xp of your character'''

        
        if len(args) is 1:
            character = None
        else:
            character = Character.get_user_name(args[:-1])

        xp = args[-1]

        try:
            xp = int(xp)
            if xp < 0:
                raise ValueError()
        except ValueError:
            await self.bot.say("{} is not a valid number.  Try again.".format(args[-1]))
            return

        session = sql.sql.getSession()

        try:
            char, _ = await self.get_character(session, character, self.get_user_id(ctx))
        except NoUserError:
            return

        classs = char.get_class()
        
        if classs is None:
            await self.bot.say("{} doesn't have a class yet.  You need to give them a class first".format(char.name))
            return
        
        old_xp = char.xp
        old_level = classs.get_level(old_xp)
        
        if xp == old_xp:
            await self.bot.say(util.get_random_line(config.lines.dumb))
            return
        char.xp = xp

        session.commit()

        new_level = classs.get_level(char.xp)
        if old_level is not new_level:

            await self.bot.say("{} has received {:,} xp and has leveled {} to level {} ({})".format(
                util.format_name(char.name),
                char.xp - old_xp,
                'up' if char.xp - old_xp > 0 else 'down',
                new_level,
                classs.title[new_level - 1]
            ))
            return
        

        next_level = "\nOnly {:,} xp to next level".format(classs.xp[new_level - 1] - char.xp + 1)

        await self.bot.say("{} has received {:,} xp and now has {:,} xp{}".format(
            util.format_name(char.name),
            char.xp - old_xp,
            char.xp,
            next_level if classs.max_level is not new_level else ""
        ))

    @commands.command(pass_context=True)
    async def setclass(self, ctx, *args):
        '''Change the class of the selected character.'''
        help_msg = "The possible classes are\n" + \
                    "**```\ncleric\ndruid\nfighter\npaladin\nranger\nmagic_user\n" + \
                    "illusionist\nthief\nassassin\nmonk```**"
        if len(args) is 0:
            await self.bot.say("Usage: {}setclass [character] <class>\n{}".format(config.config.prefix, help_msg))
            return

        if len(args) is 1:
            character = None
        else:
            character = Character.get_user_name(args[:-1])
        
        new_class = args[-1].lower()[:3]

        session = sql.sql.getSession()

        try:
            char, _ = await self.get_character(session, character, self.get_user_id(ctx))
        except NoUserError:
            return

        if new_class == 'cle':
            char.classname = 'cleric'
        elif new_class == 'dru':
            char.classname = 'druid'
        elif new_class == 'fig':
            char.classname = 'fighter'
        elif new_class == 'pal':
            char.classname = 'paladin'
        elif new_class == 'ran':
            char.classname = 'ranger'
        elif new_class == 'mag':
            char.classname = 'magic_user'
        elif new_class == 'ill':
            char.classname = 'illusionist'
        elif new_class == 'thi':
            char.classname = 'thief'
        elif new_class == 'ass':
            char.classname = 'assassin'
        elif new_class == 'mon':
            char.classname = 'monk'
        else:
            await self.bot.say(help_msg)
            return
        
        classs = char.get_class()

        session.commit()

        print("Set class for {} to {}".format(char.id, char.classname))

        level = classs.get_level(char.xp)

        await self.bot.say("{} is now a level {} {} {}".format(
            util.format_name(char.name),
            level,
            char.classname.capitalize(),
            classs.title[level - 1]))
            
    @commands.command(pass_context=True)
    async def charinfo(self, ctx, *args):
        '''Displays information about the character you made with !newchar.'''
        
        character = ' '.join(args).lower()
        if character == '':
            character = None

        session = sql.sql.getSession()

        try:
            char, _ = await self.get_character(session, character, self.get_user_id(ctx))
        except NoUserError:
            return

        classs = char.get_class()
        
        level = classs.get_level(char.xp)

        if classs is None:
            title = 'Classless'
        else:
            title = classs.title[level - 1]

        character = "{} the {}\n".format(util.format_name(char.name), title)
        
        stats = self.get_stats(char)


        if classs is not None:
            xp = '{}\n' * 5
            xp = xp.format(
                '-' * 20,
                self.__class__.length("Class:", util.format_name(char.classname), 20),
                self.__class__.length("XP:", '{:,}'.format(char.xp), 20),
                self.__class__.length("Next level:", '{:,}'.format(classs.xp[level] - char.xp + 1), 20) \
                    if level is not classs.max_level else \
                self.__class__.length("Next level:", 'Max', 20),
                self.__class__.length("Level:", str(level), 20)
            )
        else:
            xp = '{}\nNo class yet'.format('-' * 20)

        await self.bot.say("{}\n**```css\n{}{}```**".format(character, stats, xp))
            
    @commands.command(pass_context=True)
    async def delchar(self, ctx, *args):
        '''Deletes your character (if you made one with !newchar.)'''

        character = ' '.join(args).lower()
        if character == '':
            character = None

        user_id = ctx.message.author.id

        session = sql.sql.getSession()

        try:
            char, _ = await self.get_character(session, character, self.get_user_id(ctx))
        except NoUserError:
            return

        session.delete(char)
        session.commit()

        await self.bot.say("Successfully deleted..wait, what was his name?")

        print("Deleted a character of {}'s".format(user_id))

    @commands.command(pass_context=True)
    async def charlist(self, ctx):
        '''
        List out all of the characters you have
        '''

        user_id = ctx.message.author.id

        session = sql.sql.getSession()

        user = session.query(User_model).get(user_id)
        if user is None:
            await self.bot.say(util.get_random_line(config.lines.user_error.no_user))
            return

        characters = user.characters

        if len(characters) is 0:
            await self.bot.say(util.get_random_line(config.lines.user_error.no_char))
            return
        
        message = "Here is a list of {}'s characters\n".format(ctx.message.author.name)

        for char in characters:
            message += "- {}\n".format(util.format_name(char.name))
        
        await self.bot.say(message)
