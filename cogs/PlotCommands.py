
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

class PlotCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#
    
    ''' COMMANDS
    
    - plots command, /plots, Displays a list of how many plots you have in each location. Will also write something if that plot does not have enough energy so you can check for all plots at the same time.
    - plot command, /plot <location>, Displays information of your plots in {location}, shows how many plots are in there, all the resources available, and the amount of machines in there, as well as energy produced and energy needed.
    - plotbuy command, /plotbuy <location> {amount=1}, Buys {amount} plots in {location} for 1000c each.
    - plotcollect command, /plotcollect, Collects your daily maximum from each plot, and collects your hourly bit from machines, these are kept track of seperately.
    - plotconstruct command, /plotput <machine> <location> {amount=1}, Constructs {amount} of <machine> at <location>.
    - plottransfer command, /plottake <machine> <fromlocation> <tolocation> {amount=1}, Moves {amount} of <machine> from <fromlocation> to <tolocation>. Use location of "storage" if you want to stop using something.
    
    '''
    
    @app_commands.command(description="Shows information about all plots you have in every location.")
    async def plots(self, interaction: discord.Interaction):
        user = interaction.user
        plots = getplots(user)
        if len(plots) > 0:
            pages = []
            count = 0
            em = discord.Embed(title = "Plots 1/{}".format(math.ceil(len(plots)/18)),color=colorInfo())
            for name,plot in plots.items():
                em.add_field(name=name,value=f"{plot['number']} plots | {getplotnummachines(user,name)} machines | {getplotnumresources(user,name)} resources{'' if doesplothaveenoughenergy(user,name) else ' | More power needed!'}")
                count += 1
                if count > 17:
                    count = 0
                    pages.append(em)
                    em = discord.Embed(title = "Plots {}/{}".format(len(pages)+1, math.ceil(len(plots)/18)),color=colorInfo())
            await interaction.response.send_message(embed=em)
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have no plots.**",color=colorError()))
    
    @app_commands.command(description="Shows information about all plots you have in a location.")
    @app_commands.describe(location = "Location")
    async def plot(self, interaction: discord.Interaction, location: str):
        user = interaction.user
        plots = getplots(user)
        name = format(location)
        plot = plots[name]
        if valid_plot(name) and getplotnumber(user,name) > 0:
            pages = []
            count = 0
            em = discord.Embed(title = "Plot 1/{}".format(math.ceil(len(plots)/18)), description = f"{plot['number']} plots | {getplotnummachines(user,name)} machines | {getplotnumresources(user,name)} resources | {energproducedbyplot(user)[name]} energy produced | {energyconsumedbyplot(user)[name]} energy consumed{'' if doesplothaveenoughenergy(user,name) else ' | More power needed!'}", color=colorInfo())
            for m,num in plot["machines"].items():
                em.add_field(name=f"{num} {getPlotmachines()[m]['name']}",value=getPlotmachines()[m]["description"])
                count += 1
                if count > 17:
                    count = 0
                    pages.append(em)
                    em = discord.Embed(title = "Plot {}/{}".format(len(pages)+1, math.ceil(len(plots)/18)), description = f"{plot['number']} plots | {getplotnummachines(user,name)} machines | {getplotnumresources(user,name)} resources | {energproducedbyplot(user)[name]} energy produced | {energyconsumedbyplot(user)[name]} energy consumed{'' if doesplothaveenoughenergy(user,name) else ' | More power needed!'}",color=colorInfo())
            for r,num in plot["resources"].items():
                em.add_field(name=f"{num} {capital(r)}",value=get_item_desc(r))
                count += 1
                if count > 17:
                    count = 0
                    pages.append(em)
                    em = discord.Embed(title = "Plot {}/{}".format(len(pages)+1, math.ceil(len(plots)/18)), description = f"{plot['number']} plots | {getplotnummachines(user,name)} machines | {getplotnumresources(user,name)} resources | {energproducedbyplot(user)[name]} energy produced | {energyconsumedbyplot(user)[name]} energy consumed{'' if doesplothaveenoughenergy(user,name) else ' | More power needed!'}",color=colorInfo())
            await interaction.response.send_message(embed=em)
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have no plots there.**",color=colorError()))
    
    @app_commands.command(description="Buys a specified amount of plots at a location.")
    @app_commands.describe(location = "Location")
    @app_commands.describe(amount = "Amount")
    async def buyplot(self, interaction: discord.Interaction, location: str, amount:int = 1):
        user = interaction.user
        open_account(user)
        plots = getplots(user)
        name = format(location)
        if valid_plot(name):
            if getMap()["locations"][name]["controller"] != "Blue Republic":
                await interaction.response.send_message(embed=discord.Embed(title = "**You can only buy plots in the Blue Republic. If the land your plot is on is taken so will your plots be.**",color=colorError()))
                return
            price = 1000 * amount
            if price < update_bank(user):
                await interaction.response.send_message(embed=discord.Embed(title = "**You don't have enough money in your wallet to buy** " + format_number(amount) + " **plots. You would need** " + format_number(price) + " **coins.**",color=colorError()))
                return
            update_bank(user,-price)
            addplots(user,name,amount)
            await interaction.response.send_message(embed=discord.Embed(title = "**You just bought** " + format_number(amount) + " **plots in** " + location + " **for** " + format_number(price) + " **coins.**",color=colorTransaction()))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**That is not a valid location.**",color=colorError()))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#
    
### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(PlotCommands(bot),guilds=[discord.Object(id=490588110590181376)])