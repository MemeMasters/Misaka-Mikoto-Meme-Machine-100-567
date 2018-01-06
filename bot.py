import discord
from discord.ext.commands import bot
from discord.ext import commands
import random

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)
Token = "Mzk4NjQ0MzY1NTU3NDk3ODU2.DTBjlw.iemPtBTrA1xJiiWiAC72ZqPiV5E"

CritLines = ["Headshot!", "Critical Hit!", "Booyeah!", "Crit!", "Finish him!", "Get pwn'd!"]
CritFailLines = ["Oof", "Fatality!", "Ouch, ooch, oof your bones!", "That'll hurt in the morning..."]
Roll1D1Lines = ["...What did you think would happen?", "...Why?", "Are you ok?",  "Do you need a doctor?", "What else did you think it would be?"]

@client.event
async def on_ready():
    print("Hello Nerds")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.command(pass_context=True)
async def ping(ctx):
    await client.say("Pong!")

@client.command(pass_context=True)
async def weeb(ctx):
    await client.say("He's not a weeb!")

@client.command(pass_context=True)
async def stats(ctx):
    await client.say("**```prolog" + "\n" +
        "Strength:     " + str(random.randint(1,6)*3) + "\n" +
        "Intelligence: " + str(random.randint(1,6)*3) + "\n" +
        "Wisdom:       " + str(random.randint(1,6)*3) + "\n" +
        "Dexterity:    " + str(random.randint(1,6)*3) + "\n" +
        "Constitution: " + str(random.randint(1,6)*3) + "\n" +
        "Charisma:     " + str(random.randint(1,6)*3) + "```**"
    )

@client.command()
async def roll(QuantitySides: str):
	
	#Identify Devider
	Devider = 0
	i = 0
	while i < len(QuantitySides):
		letter = QuantitySides[i]
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
		Quantity = int(QuantitySides[:Devider])		#Identify Quantity
	except ValueError:
		Invalid = True

	try: #so right now it's testing if Quantity and Sides are actually numbers and not people trying to hurt senpai.
		Sides    = int(QuantitySides[Devider+1:])	#Identify Sides
	except ValueError:
		Invalid = True

	if Invalid == True:
		await client.say("'{}'? That's not how you roll a dice, silly! Use '!roll xDy'. \n x = Number of dice, \n y = Dice sides. \n ie: '!roll 2D6'.".format(QuantitySides))
		return

	#Check dice quantity
	if Quantity > 100:
		print("Too many dice detected. WTF?")
		await client.say("WHAAA! I can't roll that many dice, you do it!")
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
	await client.say(str(Total) + " with " + str(TotalCrits) + " crits!")
	if Quantity == 1 and Total == Sides and not Sides == 1:
		await client.say(CritLines[random.randint(0, len(CritLines)-1 )])
	if Quantity == 1 and Total == 1 and not Sides == 1:
		await client.say(CritFailLines[random.randint(0, len(CritFailLines)-1 )])
	if Total == 69:
		await client.say("Nice.")
	if Quantity == 1 and Sides == 1:
		await client.say(Roll1D1Lines[random.randint(0, len(Roll1D1Lines)-1 )])
    
@client.command(pass_context=True)
async def headpat(ctx):
	await client.say("Bye!")
	client.logout()
	raise SystemExit

@client.command()
async def push(remote: str, branch: str):
    await client.say('Pushing to {} {}'.format(branch, remote))

client.run(Token)