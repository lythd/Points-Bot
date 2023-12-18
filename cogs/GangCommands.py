
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



### GLOBALS ###

noneoffer = [None,None,"None",0,0]
storedoffer = noneoffer
noneloan = [None,None,0]
storedloan = noneoffer



### CLASS ###

class GangCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#
    
    ### LB COMMANDS ###
    
    @app_commands.command(description="Shows the top x people on the leaderboard for money.")
    @app_commands.describe(x = "Top x people")
    async def topmoney(self,interaction=discord.Interaction,x:int=10):
        users = getUsers()
        leader_board = {}
        total = []
        for user in users:
            name = users[user]["name"]
            money = users[user]["money"]
            leader_board[money] = name
            total.append(money)
        
        total = sorted(total,reverse=True)
        
        em = discord.Embed(title = "Money Leaderboard",color=colorLeaderboard())
        index,count,lastamt = 1,0,"whatever it is its certainly not this"
        for amt in total:
            if lastamt != amt: count = 0
            lastamt = amt
            names = leader_board[amt]
            if len(names) > 1:
                name = names[count]
                count += 1
            else: name = names[0]
            em.add_field(name = format_number(index) + ". " + name, value = format_number(amt), inline = False)
            if index == x:
                break
            else:
                index += 1
                
        await interaction.response.send_message(embed = em)
    
    @app_commands.command(description="Shows the top x people on the leaderboard for money.")
    @app_commands.describe(x = "Top x people")
    async def topnetworth(self,interaction=discord.Interaction,x:int=10):
        users = getUsers()
        leader_board = {}
        total = []
        for user in users:
            name = users[user]["name"]
            money = users[user]["money"] + value_of_items(users[user]["bag"])
            leader_board[money] = name
            total.append(money)
        
        total = sorted(total,reverse=True)
        
        em = discord.Embed(title = "Networth Leaderboard",color=colorLeaderboard())
        index,count,lastamt = 1,0,"whatever it is its certainly not this"
        for amt in total:
            if lastamt != amt: count = 0
            lastamt = amt
            names = leader_board[amt]
            if len(names) > 1:
                name = names[count]
                count += 1
            else: name = names[0]
            em.add_field(name = format_number(index) + ". " + name, value = format_number(amt), inline = False)
            if index == x:
                break
            else:
                index += 1
                
        await interaction.response.send_message(embed = em)
        
        
    @app_commands.command(description="Shows the top x people on the leaderboard for an item.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(x = "Top x people")
    async def topitem(self,interaction:discord.Interaction,item:str,x:int=10):
        users = getUsers()
        leader_board = {}
        total = []
        for user in users:
            name = users[user]["name"]
            if "bag" in users[user].keys():
                for thing in users[user]["bag"]:
                    if thing['item'] == format(item):
                        total_amount = thing['amount']
                        if total_amount > 0:
                            if total_amount in list(leader_board.keys()): leader_board[total_amount].append(name)
                            else: leader_board[total_amount] = [name]
                            total.append(total_amount)
                        break
        
        total = sorted(total,reverse=True)
        
        em = discord.Embed(title = capital(item) + " Leaderboard",color=colorLeaderboard())
        index,count,lastamt = 1,0,"whatever it is its certainly not this"
        for amt in total:
            if lastamt != amt: count = 0
            lastamt = amt
            names = leader_board[amt]
            if len(names) > 1:
                name = names[count]
                count += 1
            else: name = names[0]
            em.add_field(name = format_number(index) + ". " + name, value = format_number(amt), inline = False)
            if index == x:
                break
            else:
                index += 1
                
        await interaction.response.send_message(embed = em)
    
    @app_commands.command(description="Shows the top x people on the leaderboard for an item.")
    @app_commands.choices(mode = [
        Choice(name="Kills",value="Kills"),
        Choice(name="KOs",value="KOs"),
        Choice(name="Both",value="Defeats")
    ])
    @app_commands.describe(mode = "Mode")
    @app_commands.describe(mob = "Mob")
    @app_commands.describe(x = "Top x people")
    async def topmob(self,interaction:discord.Interaction,mob:str,mode:typing.Optional[str]="Defeats",x:int=10):
        users = getUsers()
        leader_board = {}
        total = []
        for user in users:
            name = users[user]["name"]
            total_amount = 0
            if "mobkills" in users[user].keys() and mode != "KOs":
                for thing in users[user]["mobkills"]:
                    if thing['mob'] == format(mob):
                        total_amount += thing['amount']
                        break
            if "mobkos" in users[user].keys() and mode != "Kills":
                for thing in users[user]["mobkos"]:
                    if thing['mob'] == format(mob):
                        total_amount += thing['amount']
                        break
            if total_amount > 0:
                leader_board[total_amount] = name
                total.append(total_amount)
        
        total = sorted(total,reverse=True)
        
        em = discord.Embed(title = capital(mob) + " " + mode + " Leaderboard",color=colorLeaderboard())
        index,count,lastamt = 1,0,"whatever it is its certainly not this"
        for amt in total:
            if lastamt != amt: count = 0
            lastamt = amt
            names = leader_board[amt]
            if len(names) > 1:
                name = names[count]
                count += 1
            else: name = names[0]
            em.add_field(name = format_number(index) + ". " + name, value = format_number(amt), inline = False)
            if index == x:
                break
            else:
                index += 1
                
        await interaction.response.send_message(embed = em)
    
    @app_commands.command(description="Shows the top x people on the leaderboard for duels.")
    @app_commands.choices(mode = [
        Choice(name="Wins",value="Wins"),
        Choice(name="Win Loss Difference",value="WLD"),
        Choice(name="Win Loss Ratio",value="WLR")
    ])
    @app_commands.describe(mode = "Mode")
    @app_commands.describe(x = "Top x people")
    async def topduels(self,interaction:discord.Interaction,mode:typing.Optional[str]="Wins",x:int=10):
        users = getUsers()
        leader_board = {}
        total = []
        for user in users:
            name = users[user]["name"]
            wins = 0; losses = 0
            if "wins" in users[user].keys(): wins = users[user]["wins"]
            if "losses" in users[user].keys() and mode != "Wins": losses = users[user]["losses"]
            amount = wins
            if mode == "WLD": amount -= losses
            elif mode == "WLR": amount /= losses if losses > 0 else 1
            if wins+losses > 0:
                leader_board[amount] = name
                total.append(amount)
        
        total = sorted(total,reverse=True)
        
        em = discord.Embed(title = "Duels " + mode + " Leaderboard",color=colorLeaderboard())
        index,count,lastamt = 1,0,"whatever it is its certainly not this"
        for amt in total:
            if lastamt != amt: count = 0
            lastamt = amt
            names = leader_board[amt]
            if len(names) > 1:
                name = names[count]
                count += 1
            else: name = names[0]
            em.add_field(name = format_number(index) + ". " + name, value = format_number(amt), inline = False)
            if index == x:
                break
            else:
                index += 1
                
        await interaction.response.send_message(embed = em)
    
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(GangCommands(bot),guilds=[discord.Object(id=490588110590181376)])