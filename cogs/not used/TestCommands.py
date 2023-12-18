
#---------------------------------------------------------------------------SETUP----------------------------------------------------------------------------------------#

### IMPORTS ###

import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from ButtonMenu import ButtonMenu
import datetime
import typing

### CLASS ###

class TestCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#

    @app_commands.command(name = "help", description = "Provides a list of commands")
    async def help(self, interaction: discord.Interaction):
        em = discord.Embed(title = "Help", color = discord.Color.green())
        em.add_field(name = "/help", value = "This command, lists all commands in a list.")
        em.add_field(name = "/hello", value = "Says hello back.")
        em.add_field(name = "/say <msg>", value = "Says the message through the bot.")
        em.add_field(name = "/item <item>", value = "Shows information about that item.")
        em.add_field(name = "/shop <category>", value = "Shows the shop, all items with a specific category, or in all categories.")
        em.add_field(name = "/shortshop <category>", value = "Shows the shop in a concise manner, all items with a specific category, or in all categories.")
        await interaction.response.send_message(f"Hey {interaction.user.mention}! Here is a list of commands:\n",embed = em)
        
    @app_commands.command(name = "hello", description = "Just says hello back")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hey {interaction.user.mention}!", ephemeral=True)

    @app_commands.command(name = "say", description = "Say something through the bot")
    @app_commands.describe(thing_to_say = "The thing you want to say")
    async def say(self, interaction: discord.Interaction, thing_to_say: str):
        await interaction.response.send_message(f"{interaction.user.name} said `{thing_to_say}`!", ephemeral=False)

    @app_commands.command(name="pagees", description = "This is a test command for pagees")
    async def pagees(self, interaction:discord.Interaction):
        pagees = [
            discord.Embed(title="pagee 1/5",color=discord.Color.red()),
            [discord.Embed(title="pagee 2.1/5",color=discord.Color.blue()),
            discord.Embed(title="pagee 2.2/5",color=discord.Color.blue())],
            discord.Embed(title="pagee 3/5",color=discord.Color.green()),
            discord.Embed(title="pagee 4/5",color=discord.Color.purple()),
            "not an embed just to test `pagee 5/5`"
        ]
        await interaction.response.send_message(embeds=pagees[0] if isinstance(pagees[0],list) else [pagees[0]], view=ButtonMenu(pagees,300,interaction.user))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#
    
    ### CLASS FUNCTIONS ###


### END FUNCTIONS ###

async def setup(bot:commands.Bot):
    await bot.add_cog(TestCommands(bot),guilds=[discord.Object(id=490588110590181376)])