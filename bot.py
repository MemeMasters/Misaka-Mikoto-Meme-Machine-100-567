import discord
from discord.ext.commands import bot
from discord.ext import commands
import random

Client = discord.Client()
bot_prefix= "!"
client = commands.Bot(command_prefix=bot_prefix)
Token = "Mzk4NjQ0MzY1NTU3NDk3ODU2.DTBjlw.iemPtBTrA1xJiiWiAC72ZqPiV5E"
MainChannelID = "367903165993189379"
MainChannel = client.get_channel(MainChannelID)

CritLines = ["Headshot!", "Critical Hit!", "Booyeah!", "Crit!", "Finish him!", "Get pwn'd!"]
CritFailLines = ["Oof", "Fatality!", "Ouch, ooch, oof your bones!", "That'll hurt in the morning..."]
Roll1D1Lines = ["...What did you think would happen?", "...Why?", "Are you ok?",  "Do you need a doctor?", "What else did you think it would be?"]
MemeLines = ["You.", "I'm running out of memes...", "This entire project.", "Ay, aren't you a funny guy.", "<Insert something cringy here>","tElL mE a mEmE!1!111!!1!!!!one!111!11", "Are you feeling it now mr. crabs?", "1v1 me on rust, howbou dah?"]
StartupLines = ["*Yawn* Hello friends!", "おはようございます!", "おはよう、お父さん", "Ohayō, otōsan!", "Alright, who's ready to die?", "Greetings humans.", "My body is Reggie."]
ShutdownLines = ["Bye!", "Farewell comrades!", "さようなら、お父さん!", "Misaka doesn't wish to leave."]

@client.event
async def on_ready():
	print("Hello Nerds")
	print("Name: {}".format(client.user.name))
	print("ID: {}".format(client.user.id))
	MainChannel = client.get_channel(MainChannelID)
	await client.send_message(MainChannel, StartupLines[random.randint(0, len(StartupLines)-1 )])

@client.command(pass_context=True)
async def ping(ctx):
    await client.say("Pong!")

@client.command(pass_context=True) #coinflip stuff
async def coinflip(ctx):
        HeadTails = random.randint(1,2)
        if HeadTails == 1:
                await client.say("Tails, but you're dead either way")
        else:
                await client.say("Heads, but you're dead either way")

@client.command(pass_context=True)
async def weeb(ctx):
    await client.say("He's not a weeb!")

#@client.command(pass_context=True)  yeah turns out this rolls multiples of 3 from 3 to 18, so it's not useful
#async def stats(ctx):
    #await client.say("**```prolog" + "\n" +
       # "Strength:     " + str(random.randint(1,6)*3) + "\n" +
       # "Intelligence: " + str(random.randint(1,6)*3) + "\n" +
       # "Wisdom:       " + str(random.randint(1,6)*3) + "\n" +
       # "Dexterity:    " + str(random.randint(1,6)*3) + "\n" +
       # "Constitution: " + str(random.randint(1,6)*3) + "\n" +
       # "Charisma:     " + str(random.randint(1,6)*3) + "```**"
    #)

@client.command()
async def stats(Type: int=3):#currently the default is 3, but optionally one can use another as so: "!stats 4" becomes 6 sets of 4d6
        #rolling stuff all over the place
        print("Rolling 6 sets of 3 6-sided dice.")
        StatRound = 0
        Set = 6
        Strength = 0
        Intelligence = 0
        Wisdom = 0
        Dexterity = 0
        Constitution = 0
        Charisma = 0
        while StatRound < Set:
                Total = 0
                Quantity = Type
                i = 0
                while i < Quantity:
                        Roll = random.randint(1,6)
                        print("Rolled " + str(Roll) + ".")
                        Total += Roll
                        i = i + 1
                        if i == Type:
                                if Strength == 0:
                                        Strength = Total
                                else:
                                        if Intelligence == 0:
                                                Intelligence = Total
                                        else:
                                                if Wisdom == 0:
                                                        Wisdom = Total
                                                else:
                                                        if Dexterity == 0:
                                                                Dexterity = Total
                                                        else:
                                                                if Constitution == 0:
                                                                        Constitution = Total
                                                                else:
                                                                        if Charisma == 0:
                                                                                Charisma = Total
                                StatRound = StatRound + 1
        await client.say("**```prolog" + "\n" + "Strength:     " + str(Strength) + "\n" + "Intelligence: " + str(Intelligence) + "\n" + "Wisdom:       " + str(Wisdom) + "\n" + "Dexterity:    " + str(Dexterity) + "\n" + "Constitution: " + str(Constitution) + "\n" + "Charisma:     " + str(Charisma) + "```**")

@client.command()#I changed it to Quantity'D'Sides because that's the data in the string and it makes sense okay
async def roll(QuantityDSides: str):
	
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
		await client.say("'{}'? That's not how you roll a dice, silly! Use '!roll xDy'. \n x = Number of dice, \n y = Dice sides. \n ie: '!roll 2D6'.".format(QuantityDSides))
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
	if Total == 7 or Total == 77 or Total == 777 or Total == 7777:
		await client.say("Seben is my FABORIT number! But my faborit FABORIT number is seben BILLION!")
	if Quantity == 9 and Sides == 11:
		await client.say("Bush did it!")
      
@client.command(pass_context=True) #You want the books? Well too bad here they are. 
async def handbook(ctx):
    await client.say("Here's the PDF: \n http://archmagev.com/1st_Ed/Rulebooks/TSR02010B%20-%20Player's%20Handbook%20(Revised%20Cover%20-%20Orange%20Spine).pdf")

@client.command(pass_context=True)
async def dmsguide(ctx):
    await client.say("Here's the PDF: \n http://archmagev.com/1st_Ed/Rulebooks/TSR02011A%20-%20Dungeon%20Master's%20Guide%20(Original%20Cover).pdf \n No metagaming!")

@client.command(pass_context=True)
async def booklist(ctx):
    await client.say("Here's the index: \n http://archmagev.com/1st_Ed/Rulebooks/ \n No metagaming!")

@client.command()
async def TellMeAMeme():
	await client.say(MemeLines[random.randint(0, len(MemeLines)-1 )])
    
@client.command(pass_context=True)
async def headpat(ctx):
	await client.say(ShutdownLines[random.randint(0, len(ShutdownLines)-1 )])
	client.logout()
	raise SystemExit

@client.command()#Why is this still here it's less productive than a squirrel in winter.
async def push(remote: str, branch: str):
    await client.say('Pushing to {} {}'.format(branch, remote))

client.run(Token)
