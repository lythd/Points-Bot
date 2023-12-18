
#---------------------------------------------------------------------------SETUP----------------------------------------------------------------------------------------#

### IMPORTS ###

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

class GeneralCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#
    
    @app_commands.command(description = "Just for ly ;)")
    async def refresh(self, interaction: discord.Interaction):
        if interaction.user.id == 325691401851633674:
            refresh()
            await interaction.response.send_message("Refreshed jsons!", ephemeral = True)
        else:
            await interaction.response.send_message("You are not ly ;)", ephemeral = True)
            
    @app_commands.command(description = "Just for ly ;)")
    async def update(self, interaction: discord.Interaction):
        if interaction.user.id == 325691401851633674:
            update()
            await interaction.response.send_message("Updated jsons!", ephemeral = True)
        else:
            await interaction.response.send_message("You are not ly ;)", ephemeral = True)
    
    @app_commands.command(description="Gives you some help, and shows you some important commands.")
    @app_commands.choices(page = [
        Choice(name="General",value=0),
        Choice(name="Shop",value=1),
        Choice(name="Loans",value=2),
        Choice(name="Equipment",value=3),
        Choice(name="Map",value=4),
        Choice(name="Mining",value=5),
        Choice(name="Crafting",value=6),
        Choice(name="Fishing",value=7),
        Choice(name="Fighting",value=8),
        Choice(name="Quests",value=9),
        Choice(name="Plots",value=10),
        Choice(name="Factories",value=11),
        Choice(name="Stalls",value=12),
        Choice(name="Gangs",value=13),
        Choice(name="Elections",value=14),
        Choice(name="Wars",value=15)
    ])
    @app_commands.describe(page = "Page")
    async def help(self, interaction: discord.Interaction, page: typing.Optional[int] = 0):
        pages = []
        
        em = discord.Embed(title = "Help (1/16) : General", color = colorInfo(), description = "Welcome to the Help Menu, if you are ever feeling stuck this is a good place to go. If you only need a specific thing feel free to go to that specific page using the help command, otherwise you can start from the beginning. No need to read it all now, but you can look at the first few pages to get started, and you can always pick it up where you left off.\n\nEach page gives you some basic information about a topic, as well as gives you the basic commands. Arguments given using {} are optional, and will show a default value if they have one, whereas those given by <> are required.\n\nI apologise in advance for how much big the help messages get, however this is just because of how small embeds are I promise it is quick to read.\n\n\n")
        em.add_field(name = "/help {page=General}", value = "Opens up a helpful menu to show you around the bot, starts on {page}.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (2/16) : Shop", color = colorShop(), description = "The shop is the most important mechanic, take a look about the shop and buy a couple pieces of bread so you get the hang of it, don't buy too much though otherwise you won't have enough to get started.\n\nThe market's prices change as items are bought and sold. Feel free to speculate when you get a bit more money, buy low sell high! Later on this will have more of an impact as selling loads of an item decrease its price, so you will have to make sure you diversify and don't produce loads of a single thing.\n\nDon't forget to collect your daily money!\n\nThere is also the itemlist, as many items cannot be bought on the market but have to be crafted or obtained in some special way, most of these will probably have a stall open so you can buy from there, I will talk more about stalls later, for the rest it is probably obvious based on their description, but feel free to ask around. Stalls are good in general though due to the informal 95 rule, which is that since when you sell you only get 90% of the money, you can open a stall for 95% of the price and both sellers and buyers get 5% extra. So before you think about getting any pricey item I would check for stalls.\n\nI wish you luck to climb to the top of the leaderboard!\n\n\n")
        em.add_field(name = "/shop {category=All}", value = "Opens up the shop menu so you can see all the various items on the market, with their prices and descriptions, in the desired {category}.")
        em.add_field(name = "/itemlist {category=All}", value = "Opens up a list of all items so you can see all the various items, with their descriptions, in the desired {category}.")
        em.add_field(name = "/item <item>", value = "Checks information about <item>, includes price, description, but also any other stats it might have like energy, mining tier, etc.")
        em.add_field(name = "/buy <item> {amount=1}", value = "Buys {amount} of <item> from the market. Remember to check the price beforehand as you don't want to spend more money than you wanted!")
        em.add_field(name = "/sell <item> {amount=1}", value = "Sells {amount} of <item> from the market. Remember to check the price beforehand as you don't want to sell all your items for very little!")
        em.add_field(name = "/topmoney {x=10}", value = "Displays the top {x} people on the money leaderboard.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (3/16) : Loans", color = colorTransaction(), description = "If you ever get really low on money you can always request a loan from somebody. But be careful! If you can't pay it back you will go into the negatives, and be really screwed.\n\nLoan payments are 10% for 11 days, and you can't get a loan from the same person until your previous one is fully paid off.\n\nIt might be a good idea to get a loan of around 500, as they payments are 50, and your daily beg gives you 50 on average, this way even if you fail to earn any money, you should still be good.\n\nIt might be a good idea to check out the leaderboard to see who has lots of money that can spare some, some at the top might even just give you the money without doing the loan since they have so much!\n\n\n")
        em.add_field(name = "/requestloan <person> <amount>", value = "Requests a loan of <amount> from <person>, they will have to accept or reject it.")
        em.add_field(name = "/cancelloan", value = "Cancels a loan request that you sent.")
        em.add_field(name = "/rejectloan", value = "Rejects a loan request that was sent to you.")
        em.add_field(name = "/acceptloan", value = "Accepts a loan request that was sent to you.")
        em.add_field(name = "/topmoney {x=10}", value = "Displays the top {x} people on the money leaderboard.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (4/16) : Equipment", color = colorEquipment(), description = "Although this game is based on the market, there is a lot more to it than that! If you want to go mining, fishing, or fighting, you will need equipment first!\n\nThere are four slots: main, armor, accessory, and ammo. Main is for weapons, tools, and fishing rods, armor and accessory is self explanatory, ammo allows you to store ammo for fighting or bait for fishing. Although most armors and accessories are made for fighting, there are some that provide bonuses for mining or fishing.\n\nFor now we will start with mining, why don't you eat some food and buy a basic pickaxe?\n\n\n")
        em.add_field(name = "/equipment", value = "Displays your equipment and current stats, this also takes into account your location.")
        em.add_field(name = "/equip <item>", value = "Equips <item>.")
        em.add_field(name = "/consume <item>", value = "Eats/drinks <item>.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (5/16) : Map", color = colorMap(), description = "One of the biggest changes is the map, although there was a map before now its in the bot!\n\nDifferent locations will have certain benefits, like certain items that can be found only there, certain mobs that can be found there, various fishing stats, etc.\n\nI would recommend looking at the map in all the map modes to get a good idea, and then checking out a couple of places to see their specific info.\n\nWhen you are done move to a good location and get ready to start mining!\n\n\n")
        em.add_field(name = "/map {mode=Default}", value = "Displays the current map in {mode}, useful for seeing where you are.")
        em.add_field(name = "/mapinfo <location>", value = "Gives all the information about the <location>.")
        em.add_field(name = "/location", value = "Displays your current location, with its assosciated info.")
        em.add_field(name = "/move <location>", value = "Moves to the <location>.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (6/16) : Mining", color = colorMining(), description = "Now its time to mine, you can mine anywhere in the Blue Republic where there is no fighting.\n\nThere are three modes, Once, which mines a single time with your equipped pickaxe, Pickaxe, which mines through your equipped pickaxe, and All, which mines through your equipped pickaxe and every other pickaxe of that type in your bag. These modes allow mining to happen very quickly, unlike fishing and fighting which are more 'real time' and have to go one at a time.\n\nMining will stop at any time if you run out of energy, or your pickaxe breaks. The chance of your pickaxe (or any other item) breaking is 1/durability.\n\nThe basic mining loop is mine until you stop, buy food or pickaxes whichever you need, and repeat.\n\nAs you get more money you can get better pickaxes and better food. Crafting goes hand in hand with mining so check out that section too!\n\nPickaxes have three stats, durability, which we mentioned already, double ore chance, which doubles the mined ore (by ore I mean anything shown by /tiers), and tier, which determines what ores can be mined. Any other item found mining has a fixed chance and doesn't depend on the pickaxe in any way.\n\n\n")
        em.add_field(name = "/equipment", value = "Displays your equipment and current stats, this also takes into account your location.")
        em.add_field(name = "/equip <item>", value = "Equips <item>.")
        em.add_field(name = "/mine <mode>", value = "Mines in the current location with the current gear with <mode>, modes are Once, Pickaxe, and All.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (7/16) : Crafting", color = colorCrafting(), description = "Crafting is an important and easy way to save and make money.\n\nOften instead of buying a pickaxe its cheaper to buy its components and craft it.\n\nAlso crafting diamonds and emeralds into pickaxes and then selling it is more profitable, making sure to keep some pickaxes for yourself to mine with.\n\nYou should get in the habit of checking though as someone may have just sold a bunch of pickaxes and sent the price cheaper than if you bought its components and crafted it.\n\nThe recipe name usually aligns with the output item, however in cases where there are multiple ways to craft an item, or a recipe gives multiple outputs, its important to know its the recipe name.\n\nAlso important to know that the amount refers to the amount of times the recipe is crafted, so if the output gives more than one of an item you will get more than the amount you entered.\n\n\n")
        em.add_field(name = "/recipes {category=All}", value = "Checks all recipes in the {category}, the recipe category is usually the same as the category of the output item.")
        em.add_field(name = "/craft <recipe> {amount=1}", value = "Crafts <recipe> {amount} times.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (8/16) : Fishing", color = colorFishing(), description = "When you are bored of mining its time to fish.\n\nFishing is typically best done when you have a fair bit of money and can buy expensive baits for high risk high reward.\n\nOnce you are topped off with your equipment and energy, I recommend the 4 20 rule, you leave 20% of your money, and with the remaining money you buy atleast 4 of the most expensive pieces of bait you can get, then fish it all in the best spot you can.\n\nWith four pieces you shouldn't go unlucky, but even if you do you you should have enough to go mining and get back into things.\n\nIn fishing fishing power is the most important, it determines what you can catch, as well as giving a boost to rarer items. For maximum boost the item should have a required fishing power of 75% that of your fishing power, above that its still too rare, and below that its deprioritised.\n\nAnother fishing stat is line break chance, basic rods have a 10% chance to break the line and not catch anything (still using energy and durability), but the best rods have a 0% chance.\n\nThe last fishing stat is bait consumption, basic rods have 100% consumption chance, but the best rods only have a 20% chance to consume bait.\n\nRemember that location, armor, and accessories, can all affect fishing stats, not just the rod and bait.\n\n\n")
        em.add_field(name = "/equipment", value = "Displays your equipment and current stats, this also takes into account your location.")
        em.add_field(name = "/equip <item>", value = "Equips <item>.")
        em.add_field(name = "/fish", value = "Fishes in the current location with the current gear.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (9/16) : Fighting", color = colorFighting(), description = "If you aren't having much luck fishing maybe its time to try fighting.\n\nThere are a lot of weapons, armor, and accessories, available for fighters, so unlike mining and fishing there is lots of room for customization not just picking the most expensive one.\n\nThere are 5 stats that are important for fighting: piercing damage, blunt damage, health, defense, and speed.\n\nPiercing damage (think sword or spear) can be stopped by armor (specifically the defense is subtracted from piercing damage), so is better for lightly defensive foes. Whereas blunt damage is irrespective of defense. Specific weapons can have both, but most only have one or the other. Accessories and armor can boost damage overall, or a specific type of damage, regardless it cannot boost damage of a type not used. Ie if a spear is pure piercing damage, even if your accessory boosts blunt damage by 10, you will not do any blunt damage as you have nothing to do it with.\n\nHealth is how much damage you can take before you die, and defense is like an extra health bar before your actual health bar. This does mean once their armor is broken your piercing weapons will do full damage. Piercing also gets a 10% buff if they have no defense, or if there defense has been broken. Speed allows you to decide who goes first, your base speed depends on how much energy you have, 1m energy will reach the cap of 300 base speed, however 10k energy for 200 base speed is more affordable.\n\nThere are three categories of weapons, melee, ranged, and magic. Melee is about split between piercing and blunt weapons, and has the most variety. Ranged weapons require ammo of the correct ammo class (think bows go with arrows guns go with bullets), ammo does boost damage so you get additional damage based on that, ranged is mostly piercing. Magic weapons require a mana crystal in the accessory slot, which limit them to not having accessories, the mana crystal uses every time, but the magic weapons themselves have extremely high durability, so are practically never used up. Magic weapons also deal piercing damage, however they completely ignore defense, except for they still require no defense for the 10% bonus, which means any amount of defense will completely deny that bonus.\n\nFighting is probably the most complicated mechanic do don't worry if you don't get it all at first, just buy some basic equipment and try it out.\n\n\n")
        em.add_field(name = "/equipment", value = "Displays your equipment and current stats, this also takes into account your location.")
        em.add_field(name = "/equip <item>", value = "Equips <item>.")
        em.add_field(name = "/fight", value = "Fights a random enemy in the current location with the current gear.")
        em.add_field(name = "/fightdummy {piercing=-1} {blunt=-1} {health=300} {defense=0} {speed=100}", value = "Fights a dummy to test out your gear, no items will break or be consumed.")
        em.add_field(name = "/duel <player> <money> {gang=False}", value = "Sends a duel request to <player> for <money>, {gang} is whether it counts as a gang duel.")
        em.add_field(name = "/duelaccept", value = "Accepts a duel, and a fight occurs, make sure to equip before accepting.")
        em.add_field(name = "/duelreject", value = "Rejects a duel.")
        em.add_field(name = "/duelcancel", value = "Cancels a duel.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (10/16) : Quests", color = colorQuest(), description = "Every day there is a new quest item that can only be obtained on that day. Check it out to see what location it is in, and whether you need to mine, fish, or fight to obtain it.\n\nQuests give you a sizeable reward and there is a quest leaderboard.\n\nYou can collect multiple quest items in a day however you cannot trade or give them to any player, and only one can be submitted every day, so collecting more than one is useless.\n\n\n")
        em.add_field(name = "/topquests {x=10}", value = "Displays the top {x} people on the quest leaderboard.")
        em.add_field(name = "/questview", value = "Views the daily quest item.")
        em.add_field(name = "/questsubmit", value = "Submits a daily quest item for a reward, can only be done once a day.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (11/16) : Plots", color = colorPlot(), description = "Once you get some money its time to buy some plots to get some resources.\n\nYou basically just wanna start by buying plots at certain locations. Each location has a few resources that it has, each of them with a min and max amount that will be in each plot bought. Locations also have other info like how windy it is or how sunny it is.\n\nBuying more than one plot of the same type in the same location just merges all of them into a bigger plot with its collective resources. \n\nThen you are able to collect a basic daily amount from those resources (10 of each item type, and not all resources can be collected, like oil has to be drilled), this amount represents what you harvest yourself, so its a small amount.\n\nYou can check up on this every day and collect and sell the amounts.\n\nIt is calculated to the previous hour based on the last update, and changing anything about your plots will automatically collect before, so its a good idea to wait until just after a number of hours from the last update. Ie if you bought a cow farm at 8:14am and its now 3:05pm don't do anything yet, wait until 3:15pm just to be safe. It's not a big deal but might as well.\n\nHowever plots get a lot faster once you can get some machines, machines can be bought from other people or made in factories. Machines drastically improve performance. Machines require power, a unit of energy (EU) is equal to 1 lampoil or 1 coal, and machines require a certain amount every hour, if the total machine power needed in a plot is not met then no machines will collect anything in that plot. Power must be generated on that plot (remember plots will be automatically merged), any excess oil or coal produced can be collected by the player. Wind and Solar are also options but they don't give any resources if you have excess power, and depend on how windy and sunny it is in that location.\n\n\n")
        em.add_field(name = "/plotlist", value = "Displays a list of every plot type.")
        em.add_field(name = "/plots {location=All}", value = "Displays a list of all of your plots in {location}.")
        em.add_field(name = "/plotbuy <location> <plot> {amount=1}", value = "Buys {amount} of <plot> in {location}.")
        em.add_field(name = "/plotsell <location> <plot> {amount=1}", value = "Sells {amount} of <plot> in {location}.")
        em.add_field(name = "/plotcollect", value = "Collects from every plot, can be used every hour.")
        em.add_field(name = "/plotput <machine> <location> <plot> {amount=1}", value = "Puts {amount} of <machine> in <plot> at <location>.")
        em.add_field(name = "/plottake <machine> <location> <plot> {amount=1}", value = "Takes {amount} of <machine> from <plot> at <location>.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (12/16) : Factories", color = colorFactory(), description = "At last, the industrial revolution! Factories allow you to make complicated machines for plots and other factories, as well as certain items that are too complicated to craft, like metal bars from ores.\n\nThere are a lot of factories and knowing what you need to make what can be complicated, so use /factorytiers to get a good view on progression. Factories on each tier can be made entirely from factories on the tier below. This isn't a strict rule though if you can get certain parts from someone else you can skip that.\n\nOnce you have a good luck and know what factory to start with, you can make that factory. Making works a lot like crafting however the result isn't an item its a factory, and you will always get one of a single type of a factory.\n\nAfter that you can use a factory to get items, keep in mind it may produce more than one item at a time so the total amount is not necessarily the same. Factories typically produce a single type of item but can produce more. Sometimes the factory name is the same as the item, but in other cases it might not be, so make sure you know.\n\n\n")
        em.add_field(name = "/factorylist", value = "Displays a list of every factory type.")
        em.add_field(name = "/factorytiers", value = "Displays a list of every factory type in a tiered format to understand progression.")
        em.add_field(name = "/factories", value = "Displays a list of all of your factories.")
        em.add_field(name = "/factorymake <factory> {amount=1}", value = "Makes {amount} of <factory>.")
        em.add_field(name = "/factoryuse <factory> {amount=1}", value = "Uses a <factory> {amount> times.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (13/16) : Stalls", color = colorTransaction(), description = "A lot of factory items, and special items, cannot be sold on the market. If you want to sell them you can sell them to another player using a stall or an offer.\n\nYou can open a stall which is basically just a place for you to put items up at a price. You can have stalls either be Gang-Only or Public, more on gangs later.\n\nBuying from stalls is a great way to get items you would otherwise find hard to get, like items locked behind a factory you don't have.\n\nBuying from stalls will automatically choose the cheapest stall that can sell as many items as you have, so make sure you check carefully so you know which you are buying from and don't spend way too much money because the cheaper stall didn't have enough.\n\nStalls are considered not available if they do not have any items, enough items, or due to being gang-only and you not apart of that gang you are blocked from that stall.\n\n\n")
        em.add_field(name = "/stalllist {category=All}", value = "Looks at the list of available stalls for {category}.")
        em.add_field(name = "/stallview <item> {amount=1}", value = "Looks at the cheapest available stall for {amount} of <item>.")
        em.add_field(name = "/stallbuy <item> {amount=1}", value = "Buys from the cheapest available stall {amount} of <item>.")
        em.add_field(name = "/stalls", value = "Looks at all your stalls.")
        em.add_field(name = "/stallopen <item> <price> {mode=Public}", value = "Opens a stall for <item> at <price> with {mode}.")
        em.add_field(name = "/stalldeposit <item> {amount=1}", value = "Deposits {amount} of <item> in your stall.")
        em.add_field(name = "/stallwithdraw <item> {amount=1}", value = "Withdraws {amount} of <item> in your stall.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (14/16) : Gangs", color = colorGang(), description = "Gangs have been brought back! Gangs are a group of dedicated people trying to dominate the leaderboards together. We are still friendly to eachother, and there is nothing personal, but we have a friendly rivalry to see who can be on top.\n\nThere are various things gangs can compete over, whether its places on money or items leaderboard, most total money, most total members, gang duel stats, and prestige. Prestige is my way of calculating a single metric based on everything else, however you may not value things the same way as mine so its not the be all and end all, and you shouldn't join a gang solely on its prestige, join one that will be the best for you.\n\nGangs will have lots of gang exclusive stalls, likely selling items for cheap to help you out. Gangs also will have various specialties, for example a fishing gang, which has lots of fishing equipment they can sell you for cheap in their stalls, so if you are into fishing you would join them. The gang will likely say this in their description, as well as a list of achievements. Don't be afraid to give smaller less impressive gangs a shot too, they will probably give you more in benefits than the bigger ones!\n\n\n")
        em.add_field(name = "/topmoney {x=10}", value = "Displays the top {x} people on the money leaderboard.")
        em.add_field(name = "/topitem <item> {x=10}", value = "Displays the top {x} people on the <item> leaderboard.")
        em.add_field(name = "/topgangs {x=10}", value = "Displays the top {x} gangs on the gang prestige leaderboard.")
        em.add_field(name = "/ganglist", value = "Displays a list of all gangs with descriptions and member counts.")
        em.add_field(name = "/ganginfo <gang>", value = "Displays info about a <gang>, including description, member count, total money, total quests, gang duel wins, gang duel losses, and prestige.")
        em.add_field(name = "/gangjoin <gang>", value = "Joins <gang>, leaves any gang you were in before.")
        em.add_field(name = "/gangleave", value = "Leaves your gang.")
        em.add_field(name = "/duel <player> <money> {gang=False}", value = "Sends a duel request to <player> for <money>, {gang} is whether it counts as a gang duel.")
        em.add_field(name = "/duelaccept", value = "Accepts a duel, and a fight occurs, make sure to equip before accepting.")
        em.add_field(name = "/duelreject", value = "Rejects a duel.")
        em.add_field(name = "/duelcancel", value = "Cancels a duel.")
        pages.append(em)
        
        em = discord.Embed(title = "Help (15/16) : Elections", color = colorElection(), description = "Although elections are handled outside the bot, they do have various effects inside the bot.\n\nElections are for the President of the Blue Republic! Remember although we may have friendly rivalries, we are part of the same country, and have actual enemies from outside we collectively compete against.\n\nSometimes candidates will be NPCs, but othertimes they will be players. There will be some election debates, so feel free to send up questions for our candidates. Each candidate will give some kind of boost, and potentially some kind of drawback if the boost is too powerful.\n\nI will try to implement some fun events based on elections.\n\n\n")
        pages.append(em)
        
        em = discord.Embed(title = "Help (16/16) : Wars", color = colorWar(), description = "One of the main events its wars, although there are always border conflicts so you can fight, sometimes there will be an all out battle, and perhaps multiple if its a big war.\n\nA war does not necessarily mean there is a battle going on, I will likely have battles happening on weekends where more people can be active.\n\nThe way a battle will work is they will have x amount of certain mobs, like 100 zombies and 40 skeletons, and we have to collectively beat all of them in a day. If a day passes and we do not beat them then we lose that battle and then lose that location, if we do beat all of them then we win the battle and win the location.\n\nGaining and losing land has effects for all of us, so we all need to work together and help eachother.\n\nFighting as normal on the location is seperate to battling and will still work as normal, so remember to battle and not fight.\n\nAlso if you have tanks you can battle using those, each tank will kill a random number from 0 to 10 enemies.\n\n\n")
        em.add_field(name = "/battle", value = "Battles an enemy as part of the war, you need to be in the right location.")
        em.add_field(name = "/tankbattle", value = "Battles enemies using a tank as part of the war, you need to be in the right location.")
        pages.append(em)
        
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[page],list) else [pages[page]], view=ButtonMenu(pages,600,interaction.user,page))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no help command could be found.",color=colorError()))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(GeneralCommands(bot),guilds=[discord.Object(id=490588110590181376)])