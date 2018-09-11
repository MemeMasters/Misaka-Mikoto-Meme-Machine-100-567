import os
import random
import json

from discord.ext import commands

from dm_assist.config import config

dumbLines = config['lines']['dumb']

class RolePlay:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def stats(self, ctx, Quantitystr: str=3, Setstr: str=7):#currently the default is 3, but optionally one can use another as so: "!stats 4" becomes 6 sets of 4d6
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
                    await  self.bot.say("...I have no idea what you meant by that. \n Usage: !stats (Number of dice per stat) (Number of stats) \n (If you use more than three dice per stat, only the top 3 will be used.)")
                    return
        
            if Quantity >100:
                    await  self.bot.say("WHAAA! I can't roll that many dice, you do it!")
                    return

            if Set >10:
                    await  self.bot.say("I'm not gonna roll that many stats, do it yourself!")
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
            await  self.bot.say("**```css" + "\n" + "Strength:     " + str(Strength) + "\n" + "Intelligence: " + str(Intelligence) + "\n" + "Wisdom:       " + str(Wisdom) + "\n" + "Dexterity:    " + str(Dexterity) + "\n" + "Constitution: " + str(Constitution) + "\n" + "Charisma:     " + str(Charisma) + "\n" + "Comeliness    " + str(Comeliness) + "```**")
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
                            await  self.bot.say("Stats saved to character.")
                    else:
                            await  self.bot.say("Your character already has stats. Stats not overwritten")
            else:
                    await  self.bot.say("No character detected. Stats not applied.")


    @commands.command()#I changed it to Quantity'D'Sides because that's the data in the string and it makes sense okay
    async def roll(self, QuantityDSides: str):
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
            await  self.bot.say("'{}'? That's not how you roll a dice, silly! Use '!roll xDy'. \n x = Number of dice, \n y = Dice sides. \n ie: '!roll 2D6'.".format(QuantityDSides))
            return

        #Check dice quantity
        if Quantity > 10000:
            print("Too many dice detected. WTF?")
            await  self.bot.say("WHAAA! I can't roll that many dice, you do it!")
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
        await  self.bot.say(str(Total))# + " with " + str(TotalCrits) + " crits!")
        #if Quantity == 1 and Total == Sides and not Sides == 1:
            #await  self.bot.say(CritLines[random.randint(0, len(CritLines)-1 )])
        #if Quantity == 1 and Total == 1 and not Sides == 1:
            #await  self.bot.say(CritFailLines[random.randint(0, len(CritFailLines)-1 )])
        if Total == 69:
            await  self.bot.say("Nice.")
        if Quantity == 1 and Sides == 1:
            await  self.bot.say(dumbLines[random.randint(0, len(dumbLines)-1 )])
        if Total == 7 or Total == 77 or Total == 777 or Total == 7777:
            await  self.bot.say("Seben is my FABORIT number! But my faborit FABORIT number is seben BILLION!")
        if Quantity == 9 and Sides == 11:
            await  self.bot.say("Bush did it!")
        if Total == 420:
            await  self.bot.say("(insert bad weed joke here)")


    @commands.command(pass_context=True)
    async def newchar(self, ctx, name):
        """This command creates a character unique to your Discord user id. Usage: !newchar [Name]"""
        if os.path.isfile(ctx.message.author.id + ".json"):
            await  self.bot.say("Ayy lmao you already got a character!")
        else:
            charname = {'Name': name}
            print(charname)
            print(charname['Name'])
            out_file = open(ctx.message.author.id + ".json", "w+")
            json.dump(charname, out_file, indent=4)
            out_file.close()
            await  self.bot.say("And thus " + name + " was born")


    @commands.command(pass_context=True)
    async def level(self, ctx, level):
        '''Tests if my .json file understanding is correct'''
        Invalid = False
        try:
            level = int(level)
        except ValueError:
            Invalid = True
        if Invalid == True:
            await  self.bot.say("That's not a valid level")
            return
        if level == 1 or level == 2 or level == 3 or level == 4:
            if os.path.isfile("Classes.json"):
                in_file = open("Classes.json")
                classes = json.load(in_file)
                in_file.close()
                await  self.bot.say("Your cleric is level " + str(level) + ".\n" +
                "You have " + str(classes[0]["levels"][str(level)]["exp"]) + " exp.\n" +
                "Your first level spells per day is " + str(classes[0]["levels"][str(level)]["spells"]["1"]) + ".\n" +
                "You turn a Shadow on a " + str(classes[0]["levels"][str(level)]["turn_tables"]["shadow"]) + ".")
        else:
            await  self.bot.say("That's not a valid level")


    @commands.command(pass_context=True)
    async def char(self, ctx):
        '''Displays information about the character you made with !newchar.'''
        if os.path.isfile(ctx.message.author.id + ".json"):
            in_file = open(ctx.message.author.id + ".json", "r")
            characterinfo = json.load(in_file)
            in_file.close()
            print(characterinfo)
            if len(characterinfo) <2:
                await  self.bot.say("**```prolog" + "\n" +
                "Name:         " + characterinfo['Name'] +
                    "```**")
            else:
                await  self.bot.say("**```css" + "\n" +
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
            await  self.bot.say("You don't have a character.")


    @commands.command(pass_context=True)
    async def delchar(self, ctx):
        '''Deletes your character (if you made one with !newchar.)'''
        if os.path.isfile(ctx.message.author.id + ".json"):
            in_file = open(ctx.message.author.id + ".json", "r")
            characterinfo = json.load(in_file)
            in_file.close()
            await  self.bot.say("Gonna delet " + characterinfo['Name'] + ".")
            os.remove(ctx.message.author.id + ".json")
        else:
            await  self.bot.say("Ain't got no character you deadbeat!")


    @commands.command(pass_context=True) #coinflip stuff
    async def coinflip(self, ctx):
        '''Flips a coin.'''
        HeadTails = random.randint(1,2)
        if HeadTails == 1:
            await  self.bot.say("Tails, but you're dead either way")
        else:
            await  self.bot.say("Heads, but you're dead either way")