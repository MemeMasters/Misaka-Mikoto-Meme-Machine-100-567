import os
import json

from discord.ext import commands

from dm_assist.config import config
from dm_assist import util

from dm_assist import sql
from dm_assist.sql.roleplay_model import Character as Character_model, User as User_model

from dm_assist import handbook


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

    def get_stats(self, character: handbook.Character):
        base = '{}\n' * 7

        def format_stat(string, stat, mod):
            stat_str = self.__class__.length(string + ":", str(stat + mod), 20)
            mod = ' ({} {}{})'.format(stat, '+' if mod > 0 else '-', abs(mod)) if mod is not 0 else ''
            return stat_str + mod

        stats = base.format(
            format_stat('Strength', character.stats.str, character.stats_mod.str),
            format_stat('Intelligence', character.stats.int, character.stats_mod.int),
            format_stat('Wisdom', character.stats.wis, character.stats_mod.wis),
            format_stat('Dexterity', character.stats.dex, character.stats_mod.dex),
            format_stat('Constitution', character.stats.con, character.stats_mod.con),
            format_stat('Charisma', character.stats.cha, character.stats_mod.cha),
            format_stat('Comeliness', character.stats.com, character.stats_mod.com)
        )

        return stats

    def get_character(self, session, name, user_id) -> (Character_model, User_model):
        """
        Get a character from a user.

        :param session: the sql session to get the user from

        :param name: name of the character

        :param user_id: id of the user
        """
        user = session.query(User_model).get(user_id)
        if user is None:
            self.bot.say(util.get_random_line(config.lines.user_error.no_user))
            raise NoUserError()

        try:
            char = user.get_character(name=name)

            if char is None:
                if name is None:
                    self.bot.say(util.get_random_line(config.lines.user_error.no_char))
                else:
                    self.bot.say(util.get_random_line(config.lines.user_error.wrong_char))
                raise NoUserError()
        except sql.roleplay_model.TooManyCharactersError:
            self.bot.say(util.get_random_line(config.lines.user_error.too_many_char))
            raise NoUserError()
        
        return char, user

    # Basic character commands
    
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
    async def charinfo(self, ctx, *args):
        '''Displays information about the character you made with !newchar.'''
        
        name = ' '.join(args).lower()
        if name == '':
            name = None

        session = sql.sql.getSession()

        try:
            char, _ = self.get_character(session, name, self.get_user_id(ctx))
        except NoUserError:
            return

        character = char.get_character()
        
        classs = character.classs

        if classs is None:
            title = ''
        else:
            level = char.get_level()
            title = classs.title[level - 1]

        if character.race is not None:
            race = char.race.capitalize()
        else:
            race = ''

        name = "{} the {} {} {}\n".format(util.format_name(char.name), 'Male' if char.race else 'Female', race, title)
        
        stats = self.get_stats(char)


        if classs is not None:
            level = char.get_level()
            xp = '{}\n' * 5
            xp = xp.format(
                '-' * 20,
                self.__class__.length("Class:", util.format_name(char.classname), 20),
                self.__class__.length("XP:", '{:,}'.format(char.xp), 20),
                self.__class__.length("Next level:", '{:,}'.format(classs.xp[level - 1] - char.xp + 1), 20) \
                    if level is not classs.max_level else \
                self.__class__.length("Next level:", 'Max', 20),
                self.__class__.length("Level:", str(level), 20)
            )
        else:
            xp = ''
        
        race_str = '{}\n' * 3
        race_str = race_str.format(
            '-' * 20,
            self.__class__.length("Race:", race, 20),
            self.__class__.length("Gender:", 'Male' if char.race else 'Female', 20)
        )

        await self.bot.say("{}\n**```css\n{}{}{}```**".format(name, stats, xp, race_str))
            
    @commands.command(pass_context=True)
    async def delchar(self, ctx, *args):
        '''Deletes your character (if you made one with !newchar.)'''

        character = ' '.join(args).lower()
        if character == '':
            character = None

        user_id = ctx.message.author.id

        session = sql.sql.getSession()

        try:
            char, _ = self.get_character(session, character, self.get_user_id(ctx))
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

    # Level commands
    
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
            char, _ = self.get_character(session, character, self.get_user_id(ctx))
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

        name = Character.get_user_name(args)
        name = None if name == '' else name

        session = sql.sql.getSession()
        
        try:
            char, _ = self.get_character(session, name, self.get_user_id(ctx))
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

    # XP commands

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
            char, _ = self.get_character(session, character, self.get_user_id(ctx))
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
            char, _ = self.get_character(session, character, self.get_user_id(ctx))
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

    # Class Commands

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
            name = None
        else:
            name = Character.get_user_name(args[:-1])
        
        new_class = args[-1].lower()[:3]

        session = sql.sql.getSession()

        try:
            char, _ = self.get_character(session, name, self.get_user_id(ctx))
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
        
        character = char.get_character()

        classs = character.classs

        if character.race is not None:
            try:
                character.race.validate_class(char.classname)
            except handbook.ValidationError:
                await self.bot.say("{}s cannot be {}s".format(char.race.capitalize(), char.classname.capitalize()))
                return

        session.commit()

        print("Set class for {} to {}".format(char.id, char.classname))

        level = classs.get_level(char.xp)

        await self.bot.say("{} is now a level {} {} {}".format(
            util.format_name(char.name),
            level,
            char.classname.capitalize(),
            classs.title[level - 1]))

    # Race Commands

    @commands.command(pass_context=True)
    async def setrace(self, ctx, *args):
        '''Set the race of the selected character.'''

        usage = 'usage: {}setrace [name] [gender] <race>'.format(config.config.prefix)
        races = '**```The possible races are\ndwarf\nelf\ngnome\nhalfelf\nhalfling\nhalforc\nhuman\n```**'
        help_msg = '{}\n{}'.format(usage, races)


        if len(args) is 0:
            await self.bot.say(help_msg)
            return

        if len(args) is 1:
            name = None
            gender = None
        else:
            gender = args[-2].lower()
            if gender == 'male' or gender == 'female':
                if len(args) is 2:
                    name = None
                else:
                    name = Character.get_user_name(args[:-2])
            else:
                gender = None
                name = Character.get_user_name(args[:-1])

        race = args[-1].lower()
        if race == 'help':
            await self.bot.say(help_msg)
            return

        session = sql.sql.getSession()

        try:
            char, _ = self.get_character(session, name, self.get_user_id(ctx))
        except NoUserError:
            return
        
        if race != 'dwarf' and \
           race != 'elf' and \
           race != 'gnome' and \
           race != 'halfelf' and \
           race != 'halfling' and \
           race != 'halforc' and \
           race != 'human':
            await self.bot.say(help_msg)
            return
        
        char.race = race
        if gender is not None:
            char.gender = True if gender == 'male' else False

        from dm_assist import handbook
        from dm_assist.handbook import races

        character = char.get_character()

        if character.classs is not None:
            try:
                character.race.validate_class(char.classname)
            except handbook.ValidationError:
                await self.bot.say("{}s cannot be {}".format(util.format_name(race), util.format_name(char.classname)))
                return
        
        result = character.race.validate_stats(character.stats, character.gender)

        invalid = False
        for _, value in result.items():
            if value is not None:
                await self.bot.say(value.message)
                invalid = True
        if invalid:
            return
        
        char.stats_mod = character.race.get_Stat_modifiers()

        session.commit()

        await self.bot.say("{}\nSuccessfully changed your race to be a {} {}".format(
            util.get_random_line(config.lines.crits),
            'Male' if char.gender else 'Female',
            char.race.capitalize()
        ))

        print('Changed a characters race')

    # Stats Commands

    @commands.command(pass_context=True)
    async def rollstats(self, ctx, *args):
            '''Rolls 7 sets of 3d6, with mild flexibility. 
            Increasing the number of dice per stat will not create huge numbers, as the stats are generated from the highest three numbers rolled per set. 
            Usage: !stats [x] [y], where x is the number of dice per stat and y is the number of stats. 
            If you have made a character with !newchar, it will apply the stats rolled without confirmation unless your character already has stats.'''
            
            if len(args) is 1:
                name = None
                dice = args[0]
            elif len(args) is 0:
                name = None
                dice = '3'
            else:
                dice = args[-1]
                name = self.get_user_name(args[:-1])

            try:
                dice = int(dice)
                if dice < 3:
                    raise ValueError
            except ValueError:
                await self.bot.say("{} is not a valid number!".format(args[0]))
                return

            session = sql.sql.getSession()

            try:
                char, _ = self.get_character(session, name, self.get_user_id(ctx))
            except NoUserError:
                return
            
            
            stats = list()

            for _ in range(7):
                stats.append(util.roll_top(dice, 3, 6))

            char.strength = stats[0]
            char.intelligence = stats[1]
            char.wisdom = stats[2]
            char.dexterity = stats[3]
            char.constitution = stats[4]
            char.charisma = stats[5]
            char.comeliness = stats[6]

            character = char.get_character()

            stats_temp = char.stats

            errors = False
            if character.race is not None:
                staterrors = character.race.validate_stats(character.stats, char.gender)
                for key, error in staterrors.items():
                    if error is not None:
                        await self.bot.say("{}\nAdjusting..".format(error.message))
                        setattr(stats_temp, key, error.limit)
                        errors = True

            if errors:
                char.stats = stats_temp
                character.stats = stats_temp

            session.commit()


            message = "Set the following stats to {}\n**```css\n{}\n```**".format(
                util.format_name(char.name),
                self.get_stats(character)
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
            char, _ = self.get_character(session, character, self.get_user_id(ctx))
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
