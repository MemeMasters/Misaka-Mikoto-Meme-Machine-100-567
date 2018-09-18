import random

from discord.ext import commands

from dm_assist.config import config


class Misc:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def memberlist(self, ctx):
        '''Displays members of a server'''
        memberNames = []
        memberID = []
        membernames1 = []
        for member in ctx.message.server.members:
            members[member.id] = member
            memberNames.append(member.name)
            memberID.append(member.id)
            derp = []
            derp.append(member.name)
            derp.append(member.id)
            x = ": ".join(map(str, derp)) + "\n"
            membernames1.append(x)
        y = "".join(map(str, membernames1))
        await self.bot.say("```\n" + y + "```")

    @commands.command(pass_context=True)
    async def bored(self, ctx):
        '''For people who are bored.'''
        if ctx.message.author.id == "287697603607658496":
            await self.bot.say("Play Magic with someone!")
        else:
            await self.bot.say("Get over it.")
            print(ctx.message.author.id + " broke a rule or something")

    @commands.command(pass_context=True)
    async def weeb(self, ctx):
        '''Used to call me a weeb. Use with caution.
        There may or may not be a few lines of code allowing me to 'keep track' of you, supposing you choose to do so.'''
        await self.bot.say("He's not a weeb!")


    #@commands.command()
    #async def TellMeAMeme(self, ):
    #	'''Spits out something unfunny.'''
    #	await self.bot.say(MemeLines[random.randint(0, len(MemeLines)-1 )])

    #@commands.command(pass_context=True)
    #async def spam(self, ctx, name):
    #	'''Use this to hurt your friends. Usage: !spam [ID of target]'''
    #	if name == "287697603607658496":
    #		await self.bot.say("Nope.")
    #	else:
    #		await self.bot.say("Now spamming " + name)
            #insert all the spamming code here.

    #@commands.command()
    #async def bug_cats(self, id):
    #	'''Bug someone.'''
    #	everything = request.urlopen("https://cat-fact.herokuapp.com/facts").read().decode()
    #	jsEverything = json.loads(everything)
    #	catFacts = []
    #	for item in jsEverything["all"]:
    #		catFacts.append(item["text"])
    #	await self.bot.send_message(members[str(id)], "Thanks for subscribing to cat facts!")
    #	while True:
    #		await self.bot.wait_until_ready()
    #		await self.bot.send_message(members[str(id)], catFacts[random.randint(0, len(catFacts) - 1)])
    #		time.sleep(7)

    @commands.command(pass_context=True)
    async def headpat(self, ctx, derp: str=1):
        '''Usage: don't.'''
        if ctx.message.author.id == "287697603607658496":
            if derp == 1:
                await self.bot.say(config.lines.shutdown[random.randint(0, len(config.lines.shutdown)-1 )])
                self.bot.logout()
                self.bot.close()
                raise SystemExit
            else:
                await self.bot.say(config.lines.dumb[random.randint(0, len(config.lines.dumb) - 1)])
        else:
            await self.bot.say(config.lines.dumb[random.randint(0, len(config.lines.dumb) - 1)])


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        '''Pings the self.bot and prints your id in the output.'''
        print (ctx.message.author.id + " pinged")
        await self.bot.say("PONGU!")