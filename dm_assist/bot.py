import discord
from discord.ext import commands
import random
import asyncio
import os
import json
from urllib import request
import time

from dm_assist.config import config
from dm_assist import Bot

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus(config['voice']['opus'])


CritLines = config['lines']['crits']
CritFailLines = config['lines']['critFails']
Roll1D1Lines = config['lines']['dumb']
MemeLines = config['lines']['memes']
StartupLines = config['lines']['startup']
ShutdownLines = config['lines']['shutdown']
Character = 'test.txt'


@Bot.event
async def on_ready():
    print("Hello Nerds")
    print("Name: {}".format(Bot.user.name))
    print("ID: {}".format(Bot.user.id))
    print("___________________________")
	#MainChannel = client.get_channel(MainChannelID)
	#await client.send_message(MainChannel, StartupLines[random.randint(0, len(StartupLines)-1 )])

class Roleplay:
	"""This all creates a loose enviroment for playing Dungeons and Dragons on Discord"""
	
	@staticmethod
	def DM():
		dm = "287697603607658496"

	@staticmethod
	@Bot.command(pass_context=True)
	async def stats(ctx, Quantitystr: str=3, Setstr: str=7):#currently the default is 3, but optionally one can use another as so: "!stats 4" becomes 6 sets of 4d6
			'''Rolls 7 sets of 3d6, with mild flexibility. 
			Increasing the number of dice per stat will not create huge numbers, as the stats are generated from the highest three numbers rolled per set. 
			Usage: !stats [x] [y], where x is the number of dice per stat and y is the number of stats. 
			If you have made a character with !newchar, it will apply the stats rolled without confirmation unless your character already has stats.'''
			Invalid = False
			try:
					Quantity = int(Quantitystr)
			except ValueError:
				    Invalid = True
			try:
				    Set = int(Setstr)
			except ValueError:
				    Invalid = True
			if Invalid == True:
				    await Bot.say("...I have no idea what you meant by that. \n Usage: !stats (Number of dice per stat) (Number of stats) \n (If you use more than three dice per stat, only the top 3 will be used.)")
				    return
		
			if Quantity >100:
				    await Bot.say("WHAAA! I can't roll that many dice, you do it!")
				    return

			if Set >10:
				    await Bot.say("I'm not gonna roll that many stats, do it yourself!")
				    return#rolling stuff all over the place
			print("Rolling " + str(Set) + " sets of " + str(Quantity) + " 6-sided dice.")
			StatRound = 0
			Strength = 0
			Intelligence = 0
			Wisdom = 0
			Dexterity = 0
			Constitution = 0
			Charisma = 0
			Comeliness = 0
			while StatRound < Set:
					Total = 0
					i = 0
					Numbers = [0,0,0]
					while i < Quantity:
							Roll = random.randint(1,6)
							Numbers.extend([Roll])
							print("Rolled " + str(Roll) + ".")
							i = i + 1
							if i == Quantity:
									x = 0
									while x < 3:
											Total += max(Numbers)
											Numbers.remove(max(Numbers))
											x = x + 1
									if Strength == 0:
											Strength = Total
											print("Strength = " + str(Strength))
									else:
											if Intelligence == 0:
												    Intelligence = Total
												    print("Intelligence = " + str(Strength))
											else:
													if Wisdom == 0:
															Wisdom = Total
															print("Wisdom = " + str(Intelligence))
													else:
															if Dexterity == 0:
																    Dexterity = Total
																    print("Dexterity = " + str(Dexterity))
															else:
																	if Constitution == 0:
																		    Constitution = Total
																		    print("Constitution = " + str(Constitution))
																	else:
																			if Charisma == 0:
																				    Charisma = Total
																				    print("Charisma = " + str(Charisma))
																			else:
																					if Comeliness == 0:
																						    Comeliness = Total
																						    print("Comeliness = " + str(Comeliness))
									StatRound = StatRound + 1
			await Bot.say("**```css" + "\n" + "Strength:     " + str(Strength) + "\n" + "Intelligence: " + str(Intelligence) + "\n" + "Wisdom:       " + str(Wisdom) + "\n" + "Dexterity:    " + str(Dexterity) + "\n" + "Constitution: " + str(Constitution) + "\n" + "Charisma:     " + str(Charisma) + "\n" + "Comeliness    " + str(Comeliness) + "```**")
			if os.path.isfile(ctx.message.author.id + ".json"):
					test = 0
					in_file = open(ctx.message.author.id + ".json", "r")
					characterinfo = json.load(in_file)
					in_file.close()
					test = len(characterinfo)
					if test < 2:
						    in_file = open(ctx.message.author.id + ".json", "r")
						    characterinfo = json.load(in_file)
						    in_file.close()
						    characterinfo.update({
							    "Strength": Strength,
							    "Intelligence": Intelligence,
							    "Wisdom": Wisdom,
							    "Dexterity": Dexterity,
							    "Constitution": Constitution,
							    "Charisma": Charisma,
							    "Comeliness": Comeliness
						    })
						    out_file = open(ctx.message.author.id + ".json", "w")
						    json.dump(characterinfo, out_file, indent=4)
						    out_file.close()
						    await Bot.say("Stats saved to character.")
					else:
						    await Bot.say("Your character already has stats. Stats not overwritten")
			else:
					await Bot.say("No character detected. Stats not applied.")

	@staticmethod
	@Bot.command()#I changed it to Quantity'D'Sides because that's the data in the string and it makes sense okay
	async def roll(QuantityDSides: str):
		'''Rolls X dice with Y sides. Usage: !roll XdY'''
		#Identify Devider
		#You know it's spelled 'Divider,' right?
		Devider = 0
		i = 0
		while i < len(QuantityDSides):
			letter = QuantityDSides[i]
			if letter == "D" or letter == "d":
			    Devider = i
			i = i + 1

	    #Check formatting and tell you to screw off
		Invalid = False
		if Devider == 0:
		    Invalid = True
		Quantity = 0
		Sides = 0

		try: #"try:" tries to do the given action and if there's a non-lethal error run the code in "except ValueError" instead of crying in the output. 
		    Quantity = int(QuantityDSides[:Devider])		#Identify Quantity
		except ValueError:
		    Invalid = True

		try: #so right now it's testing if Quantity and Sides are actually numbers and not people trying to hurt senpai.
		    Sides    = int(QuantityDSides[Devider+1:])	#Identify Sides
		except ValueError:
		    Invalid = True

		if Invalid == True:
		    await Bot.say("'{}'? That's not how you roll a dice, silly! Use '!roll xDy'. \n x = Number of dice, \n y = Dice sides. \n ie: '!roll 2D6'.".format(QuantityDSides))
		    return

	    #Check dice quantity
		if Quantity > 10000:
		    print("Too many dice detected. WTF?")
		    await Bot.say("WHAAA! I can't roll that many dice, you do it!")
		    return

	    #Actually roll the dice
		print("Rolling " + str(Quantity)+ " " +str(Sides) + " sided dice.")
		Total = 0
		TotalCrits = 0
		i = 0
		while i < Quantity:
			global Canceling
			Roll = random.randint(1,Sides)
			print("Rolled " + str(Roll) + ".")
			if Roll == Sides:
				TotalCrits = TotalCrits + 1
				print("Crit!")
			Total += Roll
			i = i + 1

	    #Say the result
		print("Total is " + str(Total) + " with " + str(TotalCrits) + " crits!")
		await Bot.say(str(Total))# + " with " + str(TotalCrits) + " crits!")
		#if Quantity == 1 and Total == Sides and not Sides == 1:
		    #await Bot.say(CritLines[random.randint(0, len(CritLines)-1 )])
		#if Quantity == 1 and Total == 1 and not Sides == 1:
		    #await Bot.say(CritFailLines[random.randint(0, len(CritFailLines)-1 )])
		if Total == 69:
		    await Bot.say("Nice.")
		if Quantity == 1 and Sides == 1:
		    await Bot.say(Roll1D1Lines[random.randint(0, len(Roll1D1Lines)-1 )])
		if Total == 7 or Total == 77 or Total == 777 or Total == 7777:
		    await Bot.say("Seben is my FABORIT number! But my faborit FABORIT number is seben BILLION!")
		if Quantity == 9 and Sides == 11:
		    await Bot.say("Bush did it!")
		if Total == 420:
		    await Bot.say("(insert bad weed joke here)")

	@staticmethod
	@Bot.command(pass_context=True)
	async def newchar(ctx, name):
		"""This command creates a character unique to your Discord user id. Usage: !newchar [Name]"""
		if os.path.isfile(ctx.message.author.id + ".json"):
		    await Bot.say("Ayy lmao you already got a character!")
		else:
		    charname = {'Name': name}
		    print(charname)
		    print(charname['Name'])
		    out_file = open(ctx.message.author.id + ".json", "w+")
		    json.dump(charname, out_file, indent=4)
		    out_file.close()
		    await Bot.say("And thus " + name + " was born")

	@staticmethod
	@Bot.command(pass_context=True)
	async def level(ctx, level):
		'''Tests if my .json file understanding is correct'''
		Invalid = False
		try:
			level = int(level)
		except ValueError:
			Invalid = True
		if Invalid == True:
			await Bot.say("That's not a valid level")
			return
		if level == 1 or level == 2 or level == 3 or level == 4:
			if os.path.isfile("Classes.json"):
				in_file = open("Classes.json")
				classes = json.load(in_file)
				in_file.close()
				await Bot.say("Your cleric is level " + str(level) + ".\n" +
                "You have " + str(classes[0]["levels"][str(level)]["exp"]) + " exp.\n" +
                "Your first level spells per day is " + str(classes[0]["levels"][str(level)]["spells"]["1"]) + ".\n" +
                "You turn a Shadow on a " + str(classes[0]["levels"][str(level)]["turn_tables"]["shadow"]) + ".")
		else:
			await Bot.say("That's not a valid level")

	@staticmethod
	@Bot.command(pass_context=True)
	async def char(ctx):
		'''Displays information about the character you made with !newchar.'''
		if os.path.isfile(ctx.message.author.id + ".json"):
			in_file = open(ctx.message.author.id + ".json", "r")
			characterinfo = json.load(in_file)
			in_file.close()
			print(characterinfo)
			if len(characterinfo) <2:
			    await Bot.say("**```prolog" + "\n" +
			    "Name:         " + characterinfo['Name'] +
			      "```**")
			else:
			    await Bot.say("**```css" + "\n" +
			    "Name:         " + characterinfo['Name'] + "\n" +
			    "Strength:     " + str(characterinfo['Strength']) + "\n" +
			    "Intelligence: " + str(characterinfo['Intelligence']) + "\n" +
			    "Wisdom:       " + str(characterinfo['Wisdom']) + "\n" +
			    "Dexterity:    " + str(characterinfo['Dexterity']) + "\n" +
			    "Constitution: " + str(characterinfo['Constitution']) + "\n" +
			    "Charisma:     " + str(characterinfo['Charisma']) + "\n" +
			    "Comeliness:   " + str(characterinfo['Comeliness']) + "```**"
			    )
		else:
		    await Bot.say("You don't have a character.")

	@staticmethod
	@Bot.command(pass_context=True)
	async def delchar(ctx):
		'''Deletes your character (if you made one with !newchar.)'''
		if os.path.isfile(ctx.message.author.id + ".json"):
		    in_file = open(ctx.message.author.id + ".json", "r")
		    characterinfo = json.load(in_file)
		    in_file.close()
		    await Bot.say("Gonna delet " + characterinfo['Name'] + ".")
		    os.remove(ctx.message.author.id + ".json")
		else:
		    await Bot.say("Ain't got no character you deadbeat!")

	@staticmethod
	@Bot.command(pass_context=True) #coinflip stuff
	async def coinflip(ctx):
		'''Flips a coin.'''
		HeadTails = random.randint(1,2)
		if HeadTails == 1:
		    await Bot.say("Tails, but you're dead either way")
		else:
		    await Bot.say("Heads, but you're dead either way")

@Bot.command(pass_context = True)
async def memberlist(ctx):
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
	await Bot.say("```\n" + y + "```")

@Bot.command(pass_context=True)
async def bored(ctx):
	'''For people who are bored.'''
	if ctx.message.author.id == "287697603607658496":
		await Bot.say("Play Magic with someone!")
	else:
		await Bot.say("Get over it.")
		print(ctx.message.author.id + " broke a rule or something")

@Bot.command(pass_context=True)
async def weeb(ctx):
	'''Used to call me a weeb. Use with caution.
    There may or may not be a few lines of code allowing me to 'keep track' of you, supposing you choose to do so.'''
	await Bot.say("He's not a weeb!")


#@Bot.command()
#async def TellMeAMeme():
#	'''Spits out something unfunny.'''
#	await Bot.say(MemeLines[random.randint(0, len(MemeLines)-1 )])

#@Bot.command(pass_context=True)
#async def spam(ctx, name):
#	'''Use this to hurt your friends. Usage: !spam [ID of target]'''
#	if name == "287697603607658496":
#		await Bot.say("Nope.")
#	else:
#		await Bot.say("Now spamming " + name)
		#insert all the spamming code here.

#@Bot.command()
#async def bug_cats(id):
#	'''Bug someone.'''
#	everything = request.urlopen("https://cat-fact.herokuapp.com/facts").read().decode()
#	jsEverything = json.loads(everything)
#	catFacts = []
#	for item in jsEverything["all"]:
#		catFacts.append(item["text"])
#	await Bot.send_message(members[str(id)], "Thanks for subscribing to cat facts!")
#	while True:
#		await Bot.wait_until_ready()
#		await Bot.send_message(members[str(id)], catFacts[random.randint(0, len(catFacts) - 1)])
#		time.sleep(7)

@Bot.command(pass_context=True)
async def headpat(ctx, derp: str=1):
	'''Usage: don't.'''
	if ctx.message.author.id == "287697603607658496":
		if derp == 1:
			await Bot.say(ShutdownLines[random.randint(0, len(ShutdownLines)-1 )])
			Bot.logout()
			Bot.close()
			raise SystemExit
		else:
			await Bot.say(Roll1D1Lines[random.randint(0, len(Roll1D1Lines) - 1)])
	else:
		await Bot.say(Roll1D1Lines[random.randint(0, len(Roll1D1Lines) - 1)])


@Bot.command(pass_context=True)
async def ping(ctx):
    '''Pings the Bot and prints your id in the output.'''
    print (ctx.message.author.id + " pinged")
    await Bot.say("PONGU!")

#@Bot.event
#async def on_message(message):
#	await client.process_commands(message)
#	if not message.author.name == "BenjyBoys" or message.author.name == "Dave" or message.author.name == "DAVE":
#		#await client.send_message(message.channel, str(message.author.name) + " said " + str(message.content), tts=True)
#		print(message.author.name + ": " + message.content.lower())
#	#if message.author.name == "SUPAHSTAH VOICE":
#		#await client.send_message(message.channel, "Greetings sir.")
#		#print(message.channel.id)
#	if message.author.name == "Kikastrophe":
#		if message.content.lower() == "good Bot":
#			await client.send_message(message.channel, "Good Kik")
#		else:
#			await client.send_message(message.channel, "What did you say wench?", tts=True)

def start(token):
	Bot.run(token)
