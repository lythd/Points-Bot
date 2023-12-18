
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

class EquipCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#
    
    @app_commands.command(description="Equips an item, check p!equipment for what you have equipped.")
    @app_commands.choices(hide = [
        Choice(name="True",value=1),
        Choice(name="False",value=0)
    ])
    @app_commands.describe(item = "Item")
    @app_commands.describe(hide = "Hide")
    async def equip(self,interaction:discord.Interaction,item:str,hide:typing.Optional[int]=0):
        hide = hide == 1
        user = interaction.user
        open_account(user)
        users = getUsers()
        items = getItems()
        ind = -1
        for item_ in items:
            if format(item_['name']) == format(item):
                if item_['category'] in ['weapon','pickaxe','rod']:
                    ind = 0
                    break
                if item_['category'] == 'armor':
                    ind = 1
                    break
                if item_['category'] == 'accessory':
                    ind = 2
                    break
                if item_['category'] in ['arrow','rocket','bait']:
                    ind = 3
                    break
                await interaction.response.send_message(embed=discord.Embed(title = "**This item is not able to be equipped.**",color=colorError()),ephemeral=hide)
                return
        if ind == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Item not found.**",color=colorError()),ephemeral=hide)
            return
        res = removefrombag(user,item,1)
        if res == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**You do not have this item.**",color=colorError()),ephemeral=hide)
            return
        if users[str(user.id)]['equipment'][ind] != "None":
            addtobag(user,users[str(user.id)]['equipment'][ind],1)
        users[str(user.id)]['equipment'][ind] = format(item)
        await interaction.response.send_message(embed=discord.Embed(title = "**Equipped** " + capital(item) + " **successfully.**",color=colorGood()),ephemeral=hide)
        writeUsers()

    @app_commands.command(description="Unequips an item, check p!equipment for what you have equipped.")
    @app_commands.choices(hide = [
        Choice(name="True",value=1),
        Choice(name="False",value=0)
    ])
    @app_commands.describe(item = "Item")
    @app_commands.describe(hide = "Hide")
    async def unequip(self,interaction:discord.Interaction,item:str,hide:typing.Optional[int]=0):
        hide = hide == 1
        user = interaction.user
        open_account(user)
        users = getUsers()
        ind = -1
        for i in range(0,4):
            if users[str(user.id)]['equipment'][i] == format(item):
                ind=i           
                break
        if ind == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**You do not have this item equipped.**",color=colorError()),ephemeral=hide)
            return
        addtobag(user,item,1)
        users[str(user.id)]['equipment'][ind] = "None"
        await interaction.response.send_message(embed=discord.Embed(title = "**Unequipped** " + capital(item) + " **successfully.**",color=colorGood()),ephemeral=hide)
        writeUsers()

    @app_commands.command(description="Shows all of your stats, and equipment")
    @app_commands.choices(hide = [
        Choice(name="True",value=1),
        Choice(name="False",value=0)
    ])
    @app_commands.describe(hide = "Hide")
    async def equipment(self,interaction:discord.Interaction,hide:typing.Optional[int]=0):
        hide = hide == 1
        user = interaction.user
        stats = get_stats(user)
        em1 = generate_equipment(user.name,stats)
        em2 = generate_stats(user.name,stats)
        await interaction.response.send_message(embeds = [em1,em2],ephemeral=hide)

    @app_commands.command(description="Shows all of your stats, and equipment")
    @app_commands.choices(hide = [
        Choice(name="True",value=1),
        Choice(name="False",value=0)
    ])
    @app_commands.describe(hide = "Hide")
    async def stats(self,interaction:discord.Interaction,hide:typing.Optional[int]=0):
        hide = hide == 1
        user = interaction.user
        stats = get_stats(user)
        desc = "Shows all of your stats."
        em = generate_combined(user.name,stats)
        await interaction.response.send_message(embed = em,ephemeral=hide)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(EquipCommands(bot),guilds=[discord.Object(id=490588110590181376)])