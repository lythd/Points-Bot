
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
from functions.GeneralFunctions import *
from functions.ItemFunctions import *
from functions.UserFunctions import *
from functions.MechanicFunctions import *



### CLASS ###

class MineCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#
    
    @app_commands.command(description="Mines at the current location.")
    @app_commands.choices(mode = [
        Choice(name="Once",value="once"),
        Choice(name="Pickaxe",value="pickaxe"),
        Choice(name="All",value="all")
    ])
    @app_commands.describe(mode = "Mode")
    async def mine(self, interaction: discord.Interaction,mode:str):
        #setup
        dailylimit,itemchance,energyuse = 1000,50,3
        user = interaction.user
        oresinfo = getOres()
        users = getUsers()
        descs = []
        finale = ""
        pickaxes = 1
        pickaxesb = 0
        open_account(user)
        status,safety,controlled,air,lava,locationinfo = get_location(user)
        if status == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Mining failed since you are in an invalid location.**",color=colorError()))
            return
        if status == 1:
            descs += "You fell down to Sky City as you do not have any wings."
        if safety == 0:
            await interaction.response.send_message(embed=discord.Embed(title = "**Mining failed since you are in a foreign location.**",color=colorError()))
            return
        items = {}
        stats = get_stats(user)
        if stats['tier'] < 0:
            await interaction.response.send_message(embed=discord.Embed(title = "**Mining failed since you do not have a pickaxe equipped.**",color=colorError()))
            return
        if mode == "all": pickaxes += amountinbag(user,stats['0'])
        if users[str(user.id)]["energy"] < energyuse:
            await interaction.response.send_message(embed=discord.Embed(title = "**You do not have enough energy to mine!**",color=colorError()))
            return
        minetd,cnt = 0,0
        try:
            if str(date.today()) != users[str(user.id)]["lastmine"]:
                users[str(user.id)]["lastmine"] = str(date.today())
                users[str(user.id)]["minetd"] = 0
        except:
                users[str(user.id)]["lastmine"] = str(date.today())
                users[str(user.id)]["minetd"] = 0
        else:
            minetd = users[str(user.id)]["minetd"]
        if minetd >= dailylimit:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have hit the daily mining limit of {}. Please come again tomorrow.**".format(dailylimit),color=colorError()))
            return
        #mine loop
        tobreak = False
        while not tobreak:
            #mine
            didbreak,gotores,specamt,specdrop,specrari = mine_this(locationinfo['mining'],oresinfo,stats['tier'],stats['doc']*stats['doc-m'],stats['dur0'],(cnt+minetd+1)%itemchance==0)
            if didbreak:
                pickaxes -= 1; pickaxesb += 1
            for ore,amt in gotores.items():
                try:
                    items[ore] += amt
                except:
                    items[ore] = amt
            if specamt > 0:
                descs.append("You found {} **{}**, which is **{}** here!".format("a(n)" if specamt == 1 else "**{}** of".format(specamt),specdrop,specrari))
                try:
                    items[specdrop] += specamt
                except:
                    items[specdrop] = specamt                
            #end bits
            users[str(user.id)]["energy"] -= energyuse
            cnt += 1
            if pickaxes < 1:
                finale += "\nYou ran out of pickaxes!" if mode == "all" else "\nYour pickaxe {}!".format(break_message(stats['dur0']))
                tobreak=True
            if users[str(user.id)]["energy"] < energyuse:
                finale += "\nYou have ran out of energy!"
                tobreak=True
            if cnt + minetd >= dailylimit:
                finale += "\nYou have hit the daily mining limit of {}. Please come again tomorrow.".format(dailylimit)
                tobreak=True
            if mode == "once":tobreak=True
        #update
        if len(list(items.keys())) < 1: descs.append("You found nothing!")
        if pickaxesb > 0 and mode == "all": descs.append("You used {} of your pickaxes!".format(pickaxesb))
        if reciprocal_chance(stats['dur1']):
            if amountinbag(user,stats['0'])>0: removefrombag(user,stats['0'])
            else: users[str(user.id)]["equipment"][1] = "None"
            finale += "\nYour armor {}!".format(break_message(stats['dur1']))
        if reciprocal_chance(stats['dur2']):
            if amountinbag(user,stats['0'])>0: removefrombag(user,stats['0'])
            else: users[str(user.id)]["equipment"][2] = "None"
            finale += "\nYour accessory {}!".format(break_message(stats['dur2']))
        if pickaxesb > 0:
            if (tmpthingy := amountinbag(user,stats['0'])) < pickaxesb:
                users[str(user.id)]["equipment"][0] = "None"
                pickaxesb = tmpthingy
            removefrombag(user,stats['0'],pickaxesb)
        
        users[str(user.id)]["minetd"] += cnt
        addalltobag(user,items)
        writeUsers()
        #display
        descs = "\n".join(descs)
        descs += finale
        em = discord.Embed(title = "Mine Results", description = descs, color = colorMining())
        for item,amt in items.items():
            em.add_field(name=item,value=amt)
        await interaction.response.send_message(embed = em)
    
    
    @app_commands.command(description="Shows what pickaxes at each tier can mine.")
    async def tiers(self, interaction: discord.Interaction):
        em = discord.Embed(title = "Pickaxe Tiers", color = colorInfo())
        for tier in range(9):
            res = getAtTier(tier)
            value = ", ".join(res[0])
            if len(res[0]) > 0 and len(res[1]) > 0: value += ", "
            value += ", ".join(["{} (Reduced)".format(s) for s in res[1]])
            em.add_field(name = "Tier {}".format(tier), value = value)
        await interaction.response.send_message(f"Hey {interaction.user.mention}! Here is the list of tiers, if you want to see the pickaxes use /pickaxelist.\n",embed = em)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#
    
### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(MineCommands(bot),guilds=[discord.Object(id=490588110590181376)])