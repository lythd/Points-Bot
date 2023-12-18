
#---------------------------------------------------------------------------SETUP----------------------------------------------------------------------------------------#

### IMPORTS ###

import discord
from discord.ext import commands 
from dotenv import load_dotenv
import asyncpg
import aiohttp
import os

### BOT ###

class Ecobot(commands.Bot):
    def __init__(self, **options):
        super().__init__(command_prefix="p!", description = 'If you need additional help just ping ly#1369.', intents=discord.Intents.all(), activity=discord.Activity(type=discord.ActivityType.listening, name="you breathe"), status=discord.Status.do_not_disturb, help_command=None, **options)
    
    async def setup_hook(self):
        self.session = aiohttp.ClientSession()
        for name in os.listdir(".\\cogs"):
            if name.endswith(".py"):
                print("Loading {} ...".format(name))
                await bot.load_extension('cogs.{}'.format(name[:-3]))
        print("Syncing ...")
        await bot.tree.sync(guild = discord.Object(id=490588110590181376))
        
    async def close(self):
        await super().close()
        await self.session.close()
    
    async def on_ready(self):
        print("{} bot loaded with {}ms ping.".format(self.user.name,int(self.latency*100)))
        





































#---------------------------------------------------------------------------FINAL----------------------------------------------------------------------------------------#

os.chdir("C:\\Users\\micha\\Documents\\Coding\\blue berry\\points bot\\Points-Bot")
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = Ecobot()
bot.run(TOKEN)
