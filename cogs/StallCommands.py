
#---------------------------------------------------------------------------SETUP----------------------------------------------------------------------------------------#

### IMPORTS ###

## DISCORD ##
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

## UTILITY ##
from datetime import date
from datetime import datetime
import typing
import random
import time
import math
import copy

## MY OWN ##
from ButtonMenu import ButtonMenu
from JsonManager import *
from GeneralFunctions import *
from ItemFunctions import *
from UserFunctions import *
from MechanicFunctions import *



### CLASS ###

class StallCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#

    @app_commands.command(description="Opens a stall for an item. This costs 500 coins. Remember you can have a maximum of 5 stalls.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(price = "Price")
    @app_commands.describe(stallid = "Stall Name")
    @app_commands.describe(slogan = "Slogan")
    @app_commands.describe(gangonly = "Gang Only")
    async def openstall(self, interaction: discord.Interaction,item:str,price:int,stallid:str,slogan:str,gangonly:bool):
        stallid = capital(stallid)
        item = format(item)
        if not (valid_item(item)):
            await interaction.response.send_message(embed=discord.Embed(title = "**This is not a valid item.**",color=colorError()))
            return
        user = interaction.user
        open_account(user)
        if len(getstalls(user)) >= 5:
            await interaction.response.send_message(embed=discord.Embed(title = "**You cannot open more than 5 stalls.**",color=colorError()))
            return
        if len(getstalls(user)) > 0 and stallid in list(getstalls(user).keys()):
            await interaction.response.send_message(embed=discord.Embed(title = "**You already have a stall with that name.**",color=colorError()))
            return
        bal = update_bank(user)
        if bal < 500:
            await interaction.response.send_message(embed=discord.Embed(title = "**You need 500 coins to make a stall.**",color=colorError()))
            return
        update_bank(user,-500)
        addstall(user,stallid,item,price,slogan,gangonly)
        writeUsers()
        await interaction.response.send_message(embed=discord.Embed(title = f"**You have made a stall called** {stallid} **for** {item} **with price of** {str(price)}c **and the slogan** \"{slogan}\"**.**",color=colorTransaction()))

    @app_commands.command(description="Allows you to view and buy from the cheapest stall, I recommend you view first to check the price.")
    @app_commands.choices(mode = [
        Choice(name="Buy",value="buy"),
        Choice(name="View",value="view")
    ])
    @app_commands.describe(mode = "Mode")
    @app_commands.describe(item = "Item")
    @app_commands.describe(amount = "Amount")
    @app_commands.describe(person = "Stall Owner")
    async def stall(self, interaction: discord.Interaction,mode:str,item:str,amount:int=1,person:discord.Member=None):
        user = interaction.user
        open_account(user)
        stallowner,stallid,stall = findstall(item,amount,user.id,person.id if person != None else "")
        if stall == None:
            await interaction.response.send_message(embed=discord.Embed(title = "**Could not find a stall for that item and amount.**",color=colorError()))
            return
        cost = amount * stall[1]
        if mode == "buy":
            bal = update_bank(user)
            if bal < cost:
                await interaction.response.send_message(embed=discord.Embed(title = "**You cannot afford this, you need** " + str(cost) + " **coins.**",color=colorError()))
                return
            stall[4] -= amount
            addtobag(user,item,amount)
            update_bank(user,-cost)
            update_bank_by_id(stallowner,cost)
            updatestall(stallowner,stallid,stall)
            writeUsers()
            await interaction.response.send_message(embed=discord.Embed(title = f"**You have bought** {str(amount)} {item } **for** {str(cost)} **coins from the stall** {stallid}**.**",color=colorTransaction()))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = f"**Buying** {str(amount)} {item} **would cost** {str(cost)} **coins from the stall** {stallid}**.**",color=colorTransaction()))

    @app_commands.command(description="Toggles whether a user is blocked or not. Boycotting blocks both ways.")
    @app_commands.describe(member = "Member")
    async def stallboycott(self, interaction: discord.Interaction,member:discord.Member):
        user = interaction.user
        open_account(user)
        open_account(member)
        toggleboycott(user,member.id)
        if hasboycott(user,member.id):
            await interaction.response.send_message(embed=discord.Embed(title = "**You have boycotted** {}**.**".format(member.name),color=colorInfo()),ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have unboycotted** {}**.**".format(member.name),color=colorInfo()),ephemeral=True)

    @app_commands.command(description="Views all the users you have boycotted.")
    async def stallboycottlist(self, interaction: discord.Interaction):
        user = interaction.user
        boycottlist = getboycotts(user)
        users = getUsers()
        namelist = []
        for u,d in users.items():
            if u in boycottlist:
                namelist.append(d['name'])
        if len(namelist) > 0:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have boycotted:** {}**.**".format("**, **".join(namelist)),color=colorInfo()),ephemeral=True)
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have not boycotted anyone.**",color=colorInfo()),ephemeral=True)

    @app_commands.command(description="Views all of your stalls.")
    async def mystalls(self, interaction: discord.Interaction):
        user = interaction.user
        stalls = getstalls(user)
        if len(stalls) > 0:
            em = discord.Embed(title = "Your Stalls",color=colorInfo())
            for name,stall in stalls.items():
                em.add_field(name=name,value=f"{stall[0]} | {stall[1]}c | {stall[4]} left | {stall[2]}")
            await interaction.response.send_message(embed=em)
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have no stalls.**",color=colorError()))
        
    @app_commands.command(description="Updates a stall price.")
    @app_commands.describe(stallid = "Stall Name")
    @app_commands.describe(price = "Price")
    async def setstallprice(self, interaction: discord.Interaction,stallid:str,price:int):
        stallid = capital(stallid)
        user = interaction.user
        if not hasstall(user,stallid):
            await interaction.response.send_message(embed=discord.Embed(title = f"**You do not have a stall called** {stallid}**.**",color=colorError()))
            return
        stall = getstall(user,stallid)
        if stall == None:
            await interaction.response.send_message(embed=discord.Embed(title = f"**Could not find a stall called '{stallid}'.**",color=colorError()))
            return
        if price < 1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Stall price must be positive.**",color=colorError()))
            return
        stall[1] = price
        updatestall(str(user.id),stallid,stall)
        writeUsers()
        await interaction.response.send_message(embed=discord.Embed(title = f"**You have succesfully set** {stallid} **price at** {price}**c.**",color=colorInfo()))

    @app_commands.command(description="Deposits items into a stall.")
    @app_commands.describe(stallid = "Stall Name")
    @app_commands.describe(amount = "Amount")
    async def stalldeposit(self, interaction: discord.Interaction,stallid:str,amount:int=1):
        stallid = capital(stallid)
        user = interaction.user
        if not hasstall(user,stallid):
            await interaction.response.send_message(embed=discord.Embed(title = f"**You do not have a stall called** {stallid}**.**",color=colorError()))
            return
        stall = getstall(user,stallid)
        if stall == None:
            await interaction.response.send_message(embed=discord.Embed(title = f"**Could not find a stall called '{stallid}'.**",color=colorError()))
            return
        if amount < 1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Amount must be positive.**",color=colorError()))
            return
        if amountinbag(user,stall[0]) < amount:
            await interaction.response.send_message(embed=discord.Embed(title = "**You do not have that many items in your bag.**",color=colorError()))
            return
        stall[4] += amount
        removefrombag(user,stall[0],amount)
        updatestall(str(user.id),stallid,stall)
        writeUsers()
        await interaction.response.send_message(embed=discord.Embed(title = f"**You have succesfully deposited** {amount} {stall[0]} **from** {stallid}**.**",color=colorInfo()))
        
    @app_commands.command(description="Withdraws items from a stall.")
    @app_commands.describe(stallid = "Stall Name")
    @app_commands.describe(amount = "Amount")
    async def stallwithdraw(self, interaction: discord.Interaction,stallid:str,amount:int=1):
        stallid = capital(stallid)
        user = interaction.user
        if not hasstall(user,stallid):
            await interaction.response.send_message(embed=discord.Embed(title = f"**You do not have a stall called** {stallid}**.**",color=colorError()))
            return
        stall = getstall(user,stallid)
        if stall == None:
            await interaction.response.send_message(embed=discord.Embed(title = f"**Could not find a stall called '{stallid}'.**",color=colorError()))
            return
        if amount < 1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Amount must be positive.**",color=colorError()))
            return
        if stall[4] < amount:
            await interaction.response.send_message(embed=discord.Embed(title = "**You do not have that many items in your stall.**",color=colorError()))
            return
        stall[4] -= amount
        addtobag(user,stall[0],amount)
        updatestall(str(user.id),stallid,stall)
        writeUsers()
        await interaction.response.send_message(embed=discord.Embed(title = f"**You have succesfully withdrawn** {amount} {stall[0]} **from** {stallid}**.**",color=colorInfo()))
        
    @app_commands.command(description="Shows all stalls available to you.")
    async def stalls(self, interaction: discord.Interaction):
        user = interaction.user
        stalls = getallstalls(user)
        if len(stalls) > 0:
            pages = []
            count = 0
            em = discord.Embed(title = "Stalls 1/{}".format(math.ceil(len(stalls)/18)),color=colorInfo())
            for name,stall in stalls.items():
                em.add_field(name=name,value=f"{stall[0]} | {stall[1]}c | {stall[4]} left | {stall[2]}")
                count += 1
                if count > 17:
                    count = 0
                    pages.append(em)
                    em = discord.Embed(title = "Stalls {}/{}".format(len(pages)+1, math.ceil(len(stalls)/18)),color=colorInfo())
            await interaction.response.send_message(embed=em)
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**There are no stalls available.**",color=colorError()))
        
    @app_commands.command(description="Deletes a stall, and returns the items stored in it.")
    @app_commands.describe(stallid = "Stall Name")
    async def deletestall(self, interaction: discord.Interaction, stallid:str):
        stallid = capital(stallid)
        user = interaction.user
        if not hasstall(user,stallid):
            await interaction.response.send_message(embed=discord.Embed(title = f"**You do not have a stall called** {stallid}**.**",color=colorError()))
            return
        removestall(user,stallid)
        await interaction.response.send_message(embed=discord.Embed(title = f"**You have succesfully deleted** {stallid}**.**",color=colorInfo()))
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(StallCommands(bot),guilds=[discord.Object(id=490588110590181376)])