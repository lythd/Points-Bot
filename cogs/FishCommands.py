
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

class FishCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#
    
    @app_commands.command(description="Fishes at the current location.")
    async def fish(self, interaction: discord.Interaction):
        #setup
        dailylimit,energyuse = 30,10
        user = interaction.user
        users = getUsers()
        open_account(user)
        desc = ""
        stats = get_stats(user)
        status,safety,controlled,air,lava,locationinfo = get_location(user)
        if status == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Fishing failed since you are in an invalid location.**",color=colorError()))
            return
        if status == 1:
            desc += "You fell down to Sky City as you do not have any wings.\n"
        if safety == 0:
            await interaction.response.send_message(embed=discord.Embed(title = "**Fishing failed since you are in a foreign location.**",color=colorError()))
            return
        if lava and not 'Lava Fishing' in stats['effects']:
            await interaction.response.send_message(embed=discord.Embed(title = "**Fishing failed since you are not equipped to fish in lava.**",color=colorError()))
            return
        if stats['fp'] < 0:
            await interaction.response.send_message(embed=discord.Embed(title = "**Fishing failed since you do not have a rod and bait equipped.**",color=colorError()))
            return
        finale = ""
        if users[str(user.id)]["energy"] < energyuse:
            await interaction.response.send_message(embed=discord.Embed(title = "**You do not have enough energy to fish!**",color=colorError()))
            return
        fishtd = 0
        try:
            if str(date.today()) != users[str(user.id)]["lastfish"]:
                users[str(user.id)]["lastfish"] = str(date.today())
                users[str(user.id)]["fishtd"] = 0
        except:
                users[str(user.id)]["lastfish"] = str(date.today())
                users[str(user.id)]["fishtd"] = 0
        else:
            fishtd = users[str(user.id)]["fishtd"]
        if fishtd >= dailylimit:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have hit the daily fishing limit of {}. Please come again tomorrow.**".format(dailylimit),color=colorError()))
            return
        #fish
        rodbreak,linebreak,baitbreak,amt,item,rari = fish_this(locationinfo['fishing'],stats['fp']*stats['fp-m'],stats['lbc'],stats['bcc'],stats['dur0'])
        desc += "You found {} **{}**, which is **{}** here!".format("a(n)" if amt == 1 else "**{}** of".format(amt),item,rari)
        if 'Scary' in stats['effects'] and rari in ["Common","Uncommon"]:
            desc = "A fish came near but was spooked."
            amt = 0
        specialamt = 0
        if percentage_chance(stats['sdc']): specialamt = 1 # maybe later ill customise amount more so just leaving it here so its nice to change
        specialdrop = stats['drop']
        if specialamt > 0:
            desc += "\nYou found {} **{}**, which is a special drop because of your bait!".format("a(n)" if specialamt == 1 else "**{}** of".format(specialamt),specialdrop,)
        #end bits
        users[str(user.id)]["energy"] -= energyuse
        if users[str(user.id)]["energy"] < energyuse: finale += "\nYou have ran out of energy!"
        if 1 + fishtd >= dailylimit: finale += "\nYou have hit the daily fishing limit of {}. Please come again tomorrow.".format(dailylimit)
        #update
        if linebreak:
            desc = "You failed to catch anything as your line broke!"
            amt = 0; specialamt = 0
        if rodbreak:
            if amountinbag(user,stats['0'])>0: removefrombag(user,stats['0'])
            else: users[str(user.id)]["equipment"][0] = "None"
            finale += "\nYour rod {}!".format(break_message(stats['dur0']))
        if baitbreak:
            if amountinbag(user,stats['3'])>0: removefrombag(user,stats['3'])
            else: users[str(user.id)]["equipment"][3] = "None"
            finale += "\nYour bait has been used!"
        if reciprocal_chance(stats['dur1']):
            if amountinbag(user,stats['1'])>0: removefrombag(user,stats['1'])
            else: users[str(user.id)]["equipment"][1] = "None"
            finale += "\nYour armor {}!".format(break_message(stats['dur1']))
        if reciprocal_chance(stats['dur2']):
            if amountinbag(user,stats['2'])>0: removefrombag(user,stats['2'])
            else: users[str(user.id)]["equipment"][2] = "None"
            finale += "\nYour accessory {}!".format(break_message(stats['dur2']))
        users[str(user.id)]["fishtd"] += 1
        if item != "" and amt != 0: addtobag(user,item,amt)
        if specialdrop != "None" and specialamt != 0: addtobag(user,specialdrop,specialamt)
        writeUsers()
        #display
        desc += finale
        em = discord.Embed(title = "Fish Results", description = desc, color = colorFishing())
        if item != "" and amt != 0: em.add_field(name=item,value=amt)
        if specialdrop != "None" and specialamt != 0: em.add_field(name=specialdrop,value=specialamt)
        await interaction.response.send_message(embed = em)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#
    
### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(FishCommands(bot),guilds=[discord.Object(id=490588110590181376)])