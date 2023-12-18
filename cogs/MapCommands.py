
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

class MapCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#
    
    @app_commands.command(description="Moves to a location.")
    @app_commands.describe(location = "Location")
    async def move(self, interaction: discord.Interaction, location: str):
        try:
            data = getMap()['locations'][format(location)]
        except:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately that location could not be found.",color=colorError()))
            return
        
        user = interaction.user
        
        getUsers()[str(user.id)]['location'] = format(location)
        writeUsers()
        status,safety,controlled,air,lava,locationinfo = get_location(user)
        if status == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately your location is invalid.",color=colorError()))
            return
        if status == 1:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately you failed to fly, and fell to Sky City.",color=colorError()))
            return
        
        val = ""
        match safety:
            case 1:
                val = "There is some fighting going on, be careful!"
            case 2:
                val = "It's nice and peaceful, so I hope you have a great time!"
        if val == "":
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately you cannot travel to the foreign location of {}.".format(location),color=colorError()))
            return
        
        await interaction.response.send_message(embed=discord.Embed(title = "Succesfully moved to {}!\n{}".format(location,val),color=colorMap()))
    
    @app_commands.command(description="Displays info about your location.")
    async def location(self, interaction: discord.Interaction):
        try:
            location = getUsers()[str(interaction.user.id)]['location']
        except:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately that location could not be found.",color=colorError()))
            return
        try:
            data = getMap()['locations'][format(location)]
        except:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately that location could not be found.",color=colorError()))
            return
        pages = [generate_map_1(data),generate_map_2(data),generate_map_3(data),generate_map_4(data),generate_map_5(data)]
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no info could be found.",color=colorError()))
    
    @app_commands.command(description="Displays info about a location.")
    @app_commands.describe(location = "Location")
    async def mapinfo(self, interaction: discord.Interaction, location: str):
        try:
            data = getMap()['locations'][format(location)]
        except:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately that location could not be found.",color=colorError()))
            return
        pages = [generate_map_1(data),generate_map_2(data),generate_map_3(data),generate_map_4(data),generate_map_5(data)]
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no info could be found.",color=colorError()))
    
    @app_commands.command(description="Displays the map.")
    @app_commands.choices(mode = [
        Choice(name="Countries",value="countries"),
        Choice(name="Conflict",value="conflict"),
        Choice(name="Cities",value="cities"),
        Choice(name="Biomes",value="biomes")
    ])
    @app_commands.describe(mode = "Mode")
    async def map(self, interaction: discord.Interaction, mode: typing.Optional[str] = "countries"):
        
        em = discord.Embed(title = "**Map of Blue Island** : {} Mode".format(capital(mode)), color = colorMap(), description = getMap()['maps'][mode])
        
        match mode:
            case "countries":
                em.add_field(name = "🟦 : Ocean", value = "The peaceful ocean that surrounds us all.")
                em.add_field(name = "🟩 : Blue Republic", value = "The might of our first leader Blue took this republic from a small city to a strong nation.")
                em.add_field(name = "🟪 : Kingdom of Dungeonsia", value = "Fearing they will be conquered, they have taken the initiative and seized Blue Republic lands.")
                em.add_field(name = "🟧 : Netherian Tribes", value = "A bunch of disjointed tribes, however if they unite against a common enemy they are unstoppable.")
                em.add_field(name = "⬜ : Unclaimed", value = "The wilderness can sometimes be scarier than any country or nation.")
                em.add_field(name = "⬜ : Land", value = "Squares represent normal land.")
                em.add_field(name = "⚪ : Location", value = "Circles represent important locations like towns or cities.")
                em.add_field(name = "🤍 : Capital", value = "Hearts represent capital cities.")
            case "conflict":
                em.add_field(name = "🟦 : Ocean", value = "The peaceful ocean that surrounds us all.")
                em.add_field(name = "🟩 : Safe", value = "Safe lands allow you to gather resources peacefully.")
                em.add_field(name = "🟨 : Fighting", value = "These lands are dangerous, you can only come here to fight.")
                em.add_field(name = "🟧 : Fighting and Battle", value = "These lands are dangerous, you can only come here to fight or battle.")
                em.add_field(name = "🟥 : Battle", value = "These lands are dangerous, you can only come here to battle.")
                em.add_field(name = "⬜ : Foreign", value = "These are not our lands we cannot travel there.")
                em.add_field(name = "⬜ : Land", value = "Squares represent normal land.")
                em.add_field(name = "⚪ : Location", value = "Circles represent important locations like towns or cities.")
                em.add_field(name = "🤍 : Capital", value = "Hearts represent capital cities.")
            case "cities":
                em.add_field(name = "🟦 : Ocean", value = "")
                em.add_field(name = "🟩 : Blue Republic", value = "")
                em.add_field(name = "🟪 : Kingdom of Dungeonsia", value = "")
                em.add_field(name = "🟧 : Netherian Tribes", value = "")
                em.add_field(name = "⬜ : Unclaimed", value = "")
                em.add_field(name = "1 : Sky City", value = "")
                em.add_field(name = "2 : Dungeon City", value = "")
                em.add_field(name = "3 : Wither's Lair", value = "")
                em.add_field(name = "4 : Port City", value = "")
                em.add_field(name = "5 : Rubberport", value = "")
                em.add_field(name = "6 : Forests", value = "")
                em.add_field(name = "7 : Silk Road", value = "")
                em.add_field(name = "8 : Mines", value = "")
                em.add_field(name = "9 : Jungle", value = "")
                em.add_field(name = "10 : Smithlands", value = "")
                em.add_field(name = "11 : Fishing Ville", value = "")
                em.add_field(name = "12 : Witches Swamp", value = "")
                em.add_field(name = "13 : Fields", value = "")
                em.add_field(name = "14 : Cross Roads", value = "")
                em.add_field(name = "15 : Mineshaft", value = "")
                em.add_field(name = "16 : Nether Fortress", value = "")
                em.add_field(name = "17 : Bastion", value = "")
                em.add_field(name = "18 : Soul Valley", value = "")
                em.add_field(name = "19 : Beast's Den", value = "")
                em.add_field(name = "20 : Haven", value = "")
            case "biomes":
                em.add_field(name = "🟦 : Ocean", value = "The peaceful ocean that surrounds us all.")
                em.add_field(name = "🟩 : Plains", value = "Peaceful plains, a bit of everything, as well as lots of animals.")
                em.add_field(name = "🟢 : Location", value = "An important location you can travel to, like a town or city.")
                em.add_field(name = "💚 : Capital", value = "The capital of a country, often quite populous.")
                em.add_field(name = "🌳 : Forest", value = "Forests, tons of wood, not much else.")
                em.add_field(name = "🏖️ : Beach", value = "Not many resources here, but great for fishing.")
                em.add_field(name = "🌴 : Jungle", value = "Important resources are often found deep in the jungle.")
                em.add_field(name = "🏔️ : Mountains", value = "Great for mining, hard to invade.")
                em.add_field(name = "💧 : Swamp", value = "Hard passing through the muddy wet ground, who knows what's inside here.")
                em.add_field(name = "🔥 : Nether", value = "Blazing hot temperatures, no one wants to live in here.")
        
        await interaction.response.send_message(embed=em)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(MapCommands(bot),guilds=[discord.Object(id=490588110590181376)])