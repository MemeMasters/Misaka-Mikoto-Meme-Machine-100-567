import discord
from discord.ext.commands import bot
from discord.ext import commands
import random

#sixxx

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)

#!WEEB

CritLines = ["Headshot!", "Critical Hit!", "Oof", "Booyeah!", "Crit!"]

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
    Devider = 0
    i = 0
    while i < len(QuantitySides):
        letter = QuantitySides[i]
        if letter == "D" or letter == "d":
            Devider = i
        i = i + 1
    if Devider == 0:
        await client.say("Invalid format '{}'. Use '!roll xDy' \n x = Number of dice, \n y = Dice sides. \n IE: '!roll 2D6'.".format(QuantitySides))
        return
    Quantity = int(QuantitySides[:Devider])
    Sides    = int(QuantitySides[Devider+1:])
    print("Rolling " + str(Quantity)+ " " +str(Sides) + " sided dice.")
    if Quantity > 100:
        print("ERROR! TOO MANY DICE! BEEEEEEEEEEEEEEEEEEEEEEEEEP")
        await client.say("ERROR! TOO MANY DICE! BEEEEEEEEEEEEEEEEEEEEEEEEEP")
        return
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
    print("Total is " + str(Total) + " with " + str(TotalCrits) + " crits!")
    await client.say(str(Total) + " with " + str(TotalCrits) + " crits!")
    if Quantity == 1 and Total == Sides:
        await client.say(CritLines[random.randint(0, len(CritLines)-1 )])
    if Total == 69:
        await client.say("Nice.")
    
@client.command(pass_context=True)
async def headpat(ctx):
    await client.say("Bye!")
    raise SystemExit

@client.command()
async def push(remote: str, branch: str):
    await client.say('Pushing to {} {}'.format(branch, remote))

client.run("Mzk4NjQ0MzY1NTU3NDk3ODU2.DTBjlw.iemPtBTrA1xJiiWiAC72ZqPiV5E")



