
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

noneduel = [None,None,0,0]
storedduel = noneduel











### CLASS ###

class FightCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#
    
    ### FIGHTING COMMANDS ###
    
    ## DUELS ##
    
    @app_commands.command(description="Once a duel request has been sent to you, this command will accept it.")
    async def acceptduel(self,interaction:discord.Interaction):
        #starting checks
        global storedduel
        global noneduel
        user = interaction.user
        if storedduel == noneduel:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding duel request. If another duel request has taken place since a duel was requested from you, that duel request might have been erased.**",color=colorError()))
            return
        if user != storedduel[1]:
            await interaction.response.send_message(embed=discord.Embed(title="**You are not the intended recipient of this duel request. If another duel request has taken place since a duel was request from you, that duel request might have been erased.**",color=colorError()))
            return
        member = storedduel[0]
        users = getUsers()
        open_account(user)
        open_account(member)
        desc = []
        finale = ""
        
        #duel
        astats = get_stats(user)
        if astats['bdmg'] == -1 and astats['pdmg'] == -1:
            if 'Magic' in astats['effects']: await interaction.response.send_message(embed=discord.Embed(title = "**Duel failed since you have a magic weapon without a mana crystal.**",color=colorError()))
            else: await interaction.response.send_message(embed=discord.Embed(title = "**Duel failed since you have something thats not a weapon equipped.**",color=colorError()))
            return
        wes = weaponsuitability(astats['0']);ars = armorsuitability(astats['1']);acs = accessorysuitability(astats['2']);ams = ammosuitability(astats['3'])
        for lvl,reas in [(4,"godly"),(3,"overpowered"),(2,"inappropriate"),(1,"not-on-cycle")]:
            for var,eq in [(wes,"weapon"),(ars,"armor"),(acs,"accessory"),(ams,"ammo")]:
                if var == lvl and storedduel[3] <= var:
                    await interaction.response.send_message(embed=discord.Embed(title = "**Duel failed since your {} {} is not allowed under this duel mode.**".format(reas,eq),color=colorError()))
                    return
        bstats = get_stats(member)
        if bstats['bdmg'] == -1 and bstats['pdmg'] == -1:
            if 'Magic' in bstats['effects']: await interaction.response.send_message(embed=discord.Embed(title = "**Duel failed since they have a magic weapon without a mana crystal.**",color=colorError()))
            else: await interaction.response.send_message(embed=discord.Embed(title = "**Duel failed since they have something thats not a weapon equipped.**",color=colorError()))
            return
        wes = weaponsuitability(bstats['0']);ars = armorsuitability(bstats['1']);acs = accessorysuitability(bstats['2']);ams = ammosuitability(bstats['3'])
        for lvl,reas in [(4,"godly"),(3,"overpowered"),(2,"inappropriate"),(1,"not-on-cycle")]:
            for var,eq in [(wes,"weapon"),(ars,"armor"),(acs,"accessory"),(ams,"ammo")]:
                if var == lvl and storedduel[3] <= var:
                    await interaction.response.send_message(embed=discord.Embed(title = "**Duel failed since their {} {} is not allowed under this duel mode.**".format(reas,eq),color=colorError()))
                    return
        desc.append("{} **vs** {}".format(user.name,member.name))
        res = fight_between(astats,bstats,user.name,member.name)
        desc.append(res['logs'])
        
        #winning
        winner = 't'
        if res['astatus'] == 'Dead' and res['bstatus'] == 'Dead':
            desc.append("You both decisively knocked eachother out.")
        elif res['astatus'] == 'Dead':
            desc.append("They decisively knocked you out.")
            winner = 'b'
        elif res['bstatus'] == 'Dead':
            desc.append("You decisively knocked them out.")
            winner = 'a'
        elif res['astatus'] == 'KO' and res['bstatus'] == 'KO':
            desc.append("You both knocked eachother out.")
        elif res['astatus'] == 'KO':
            desc.append("They knocked you out.")
            winner = 'b'
        elif res['bstatus'] == 'KO':
            desc.append("You knocked them out.")
            winner = 'a'
        elif res['astatus'] == 'Exploded' and res['bstatus'] == 'Exploded':
            desc.append("You both exploded somehow.")
        elif res['astatus'] == 'Exploded':
            desc.append("You exploded somehow.")
        elif res['bstatus'] == 'Exploded':
            desc.append("They exploded somehow.")
        else:
            desc.append("The fight lasted so long that you both got tired.")
        if winner == 'a':
            finale = "**You beat them, and they had to pay you** {} **coins!**".format(storedduel[2])
            update_bank(storedduel[0],-storedduel[2])
            update_bank(storedduel[1],storedduel[2])
            addwins(user)
            addlosses(member)
            addvictories(user,member.name)
        elif winner == 'b':
            finale = "**They beat you, and you had to pay them** {} **coins!**".format(storedduel[2])
            update_bank(storedduel[1],-storedduel[2])
            update_bank(storedduel[0],storedduel[2])
            addwins(member)
            addlosses(user)
            addvictories(member,user.name)
            
        #equipment breaking
        if res['abroke0']:
            if amountinbag(user,astats['0'])>0: removefrombag(user,astats['0'])
            else: users[str(user.id)]["equipment"][0] = "None"
            finale += "\nYour weapon {}!".format(break_message(astats['dur0']))
        if res['abroke3']:
            if amountinbag(user,astats['3'])>0: removefrombag(user,astats['3'])
            else: users[str(user.id)]["equipment"][3] = "None"
            finale += "\nYour ammo has been used!"
        if res['abroke1']:
            if amountinbag(user,astats['1'])>0: removefrombag(user,astats['1'])
            else: users[str(user.id)]["equipment"][1] = "None"
            finale += "\nYour armor {}!".format(break_message(astats['dur1']))
        if res['abroke2']:
            if amountinbag(user,astats['2'])>0: removefrombag(user,astats['2'])
            else: users[str(user.id)]["equipment"][2] = "None"
            finale += "\nYour accessory {}!".format(break_message(astats['dur2']))
        if res['bbroke0']:
            if amountinbag(member,bstats['0'])>0: removefrombag(member,bstats['0'])
            else: users[str(member.id)]["equipment"][0] = "None"
            finale += "\nTheir weapon {}!".format(break_message(bstats['dur0']))
        if res['bbroke3']:
            if amountinbag(member,bstats['3'])>0: removefrombag(member,bstats['3'])
            else: users[str(member.id)]["equipment"][3] = "None"
            finale += "\nTheir ammo has been used!"
        if res['bbroke1']:
            if amountinbag(member,bstats['1'])>0: removefrombag(member,bstats['1'])
            else: users[str(member.id)]["equipment"][1] = "None"
            finale += "\nTheir armor {}!".format(break_message(bstats['dur1']))
        if res['bbroke2']:
            if amountinbag(member,bstats['2'])>0: removefrombag(member,bstats['2'])
            else: users[str(member.id)]["equipment"][2] = "None"
            finale += "\nTheir accessory {}!".format(break_message(bstats['dur2']))
        writeUsers()
        
        #display
        desc = "\n".join(desc)
        desc += finale
        em1 = generate_combined(user.name,astats)
        em2 = generate_combined(member.name,bstats)
        em3 = discord.Embed(title = "Duel", description = desc, color = colorFighting())
        
        await interaction.response.send_message("**You have been challenged by** {} **for a duel of** {} **coins, let the duel begin!**".format(member.name,storedduel[2]),embeds=[em1,em2,em3])
        storedduel = noneduel

    @app_commands.command(description="Once a duel request has been sent to you, this command will deny it.")
    async def denyduel(self,interaction:discord.Interaction):
        global storedduel
        global noneduel
        user = interaction.user
        if storedduel == noneduel:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding duel request. If another duel request has taken place since a duel was requested from you, that duel request might have been erased.**",color=colorError()))
            return
        if user != storedduel[1]:
            await interaction.response.send_message(embed=discord.Embed(title="**You are not the intended recipient of this duel request. If another duel request has taken place since a duel was request from you, that duel request might have been erased.**",color=colorError()))
            return
        storedduel = noneduel
        await interaction.response.send_message(embed=discord.Embed(title="**You have denied this duel request.**",color=colorBad()))
        
    @app_commands.command(description="Cancels a duel request you have sent.")
    async def cancelduel(self,interaction:discord.Interaction):
        global storedduel
        global noneduel
        user = interaction.user
        if storedduel == noneduel:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding duel request. If another duel request has taken place since you requested a duel, your duel request might have been erased.**",color=colorError()))
            return
        if user != storedduel[0]:
            await interaction.response.send_message(embed=discord.Embed(title="**You did not send this duel request. If another duel request has taken place since you requested a duel, your duel request might have been erased.**",color=colorError()))
            return
        storedduel = noneduel
        await interaction.response.send_message(embed=discord.Embed(title="**You have cancelled this duel request.**",color=colorBad()))

    @app_commands.command(description="Requests <member> for a duel of <money> coins, they have to type \"/acceptduel\" to accept.")
    @app_commands.describe(member = "Member")
    @app_commands.describe(money = "Bet Money")
    @app_commands.choices(mode = [
        Choice(name="Gang Duel",value=0),
        Choice(name="Current Duel Items",value=1),
        Choice(name="Any Duel Items",value=2),
        Choice(name="No Overpowered Items",value=3),
        Choice(name="No Godly Items",value=4),
        Choice(name="Anything Goes",value=5)
    ])
    @app_commands.describe(mode = "Mode")
    async def duel(self,interaction:discord.Interaction,member:discord.Member,money:int,mode:typing.Optional[int]=1):
        global storedduel
        global noneduel
        user = interaction.user
        if member.bot:
            await interaction.response.send_message(embed=discord.Embed(title="**You cannot ask a bot for a duel.**",color=colorError()))
            return
        open_account(user)
        open_account(member)
        users = getUsers()
        bal = update_bank(member)
        if bal < money:
            await interaction.response.send_message(embed=discord.Embed(title=member.name + " **does not have enough money to pay you** " + format_number(money) + "**.**",color=colorError()))
            return
        bal = update_bank(user)
        if bal < money:
            await interaction.response.send_message(embed=discord.Embed(title="**You do not have enough money to pay them** " + format_number(money) + "**.**",color=colorError()))
            return
        storedduel = [user,member,money,mode]
        await interaction.response.send_message(embed=discord.Embed(title="**You requested** "+member.name+" **for a duel of ** " + format_number(money) + " **coins. You can use /cancelduel to cancel this, and they can use /acceptduel or /denyduel to accept or deny respectively.**",color=colorFighting()))
    
    
    
    
    
    
    
    
    
    
    
    
    ## FIGHTING ##
    
    @app_commands.command(description="Tests out your kit against a dummy.")
    async def fightdummy(self, interaction: discord.Interaction, piercing:int=-1, blunt:int=-1, health:int=300, defense:int=0, speed:int=100):
        #setup
        user = interaction.user
        users = getUsers()
        open_account(user)
        stats = get_stats(user)
        if stats['bdmg'] == -1 and stats['pdmg'] == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Fighting failed since you have something thats not a weapon equipped.**",color=colorError()))
            return
        finale = ""
        desc = []
        #fight
        mobstats = {'pdmg':piercing,'bdmg':blunt,'mhp':health,'def':defense,'spd':speed,'effects':[]}
        mobstats['hp'] = mobstats['mhp']
        for s in ['tier','doc','fp','lbc','bcc','acc','dur0','dur1','dur2','dur3']:
            mobstats[s] = -1
        for s in ['critchance','mp','reg']:
            mobstats[s] = 0
        for s in ['pdmg-m','bdmg-m','doc-m','fp-m']: #multipliers
            mobstats[s] = 1
        desc.append("You are fighting a **Test Dummy!**")
        res = fight_between(stats,mobstats,user.name,"Test Dummy")
        desc.append(res['logs'])
        #update
        if res['astatus'] == 'Dead':
            desc.append("You were decisively knocked out.")
        elif res['bstatus'] == 'Dead':
            desc.append("You destroyed the Test Dummy.")
        elif res['astatus'] == 'KO':
            desc.append("You were knocked out.")
        elif res['bstatus'] == 'KO':
            desc.append("You struck down the Test Dummy.")
        elif res['astatus'] == 'Exploded':
            desc.append("You exploded somehow.")
        elif res['bstatus'] == 'Exploded':
            desc.append("The Test Dummy exploded somehow.")
        else:
            desc.append("The fight lasted so long that you got tired.")
        #display
        desc = "\n".join(desc)
        desc += finale
        em = discord.Embed(title = "Dummy Fight", description = desc, color = colorFighting())
        await interaction.response.send_message(embed = em)
    
    @app_commands.command(description="Fights an enemy at the current location.")
    async def fight(self, interaction: discord.Interaction):
        #setup
        dailylimit,energyuse = 30,50
        user = interaction.user
        users = getUsers()
        open_account(user)
        status,safety,controlled,air,lava,locationinfo = get_location(user)
        if status == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Fighting failed since you are in an invalid location.**",color=colorError()))
            return
        if status == 1:
            desc += "You fell down to Sky City as you do not have any wings.\n"
        if safety == 0:
            await interaction.response.send_message(embed=discord.Embed(title = "**Fighting failed since you are in a foreign location.**",color=colorError()))
            return
        stats = get_stats(user)
        if stats['bdmg'] == -1 and stats['pdmg'] == -1:
            if 'Magic' in stats['effects']: await interaction.response.send_message(embed=discord.Embed(title = "**Fighting failed since you have a magic weapon without a mana crystal.**",color=colorError()))
            else: await interaction.response.send_message(embed=discord.Embed(title = "**Fighting failed since you have something thats not a weapon equipped.**",color=colorError()))
            return
        finale = ""
        if users[str(user.id)]["energy"] < energyuse:
            await interaction.response.send_message(embed=discord.Embed(title = "**You do not have enough energy to fight!**",color=colorError()))
            return
        fighttd = 0
        try:
            if str(date.today()) != users[str(user.id)]["lastfight"]:
                users[str(user.id)]["lastfight"] = str(date.today())
                users[str(user.id)]["fighttd"] = 0
        except:
                users[str(user.id)]["lastfight"] = str(date.today())
                users[str(user.id)]["fighttd"] = 0
        else:
            fighttd = users[str(user.id)]["fighttd"]
        if fighttd >= dailylimit:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have hit the daily fighting limit of {}. Please come again tomorrow.**".format(dailylimit),color=colorError()))
            return
        desc = []
        #fight
        rarity = get_rarity()
        mob = random.choice(locationinfo['fighting'][rarity])
        mobinfo = getMobs()[format(mob)]
        mobstats = {s:mobinfo[s] for s in ['pdmg','bdmg','mhp','def','spd','effects']}
        mobstats['hp'] = mobstats['mhp']
        for s in ['tier','doc','fp','lbc','bcc','acc','dur0','dur1','dur2','dur3']:
            mobstats[s] = -1
        for s in ['critchance','mp','reg']:
            mobstats[s] = 0
        for s in ['pdmg-m','bdmg-m','doc-m','fp-m']: #multipliers
            mobstats[s] = 1
        desc.append("{} **{}** jumps at you, they are **{}** here!".format("A(n)" if mobinfo['type'] == "Enemy" else "The {}".format(mobinfo['type']),mobinfo['name'],rarity))
        res = fight_between(stats,mobstats,user.name,mobinfo['name'])
        desc.append(res['logs'])
        #update
        item,experience=False,False
        if res['astatus'] == 'Dead':
            desc.append("You were decisively knocked out.")
        elif res['bstatus'] == 'Dead':
            desc.append("You killed the {}.".format(mobinfo['name']))
            item = True
            experience = True
            addmobkills(user,mobinfo['name'])
        elif res['astatus'] == 'KO':
            desc.append("You were knocked out.")
        elif res['bstatus'] == 'KO':
            desc.append("You knocked out the {}.".format(mobinfo['name']))
            item = True
            addmobkos(user,mobinfo['name'])
        elif res['bstatus'] == 'Exploded':
            desc.append("The {} exploded.".format(mobinfo['name']))
        else:
            desc.append("The failed to kill the {}, and it ran away.".format(mobinfo['name']))
        if item:
            rari = get_rarity()
            drop = random.choice(list(mobinfo['drops'][rari].keys()))
            if format(drop) == 'pumpkinseed': users[str(user.id)]["pumpkinseed"] = True
            amt = parse_number(mobinfo['drops'][rari][drop])
            desc.append("It dropped {} **{}**, which is **{}** drop from it!".format("a(n)" if amt == 1 else "**{}** of".format(amt),drop,rari))
            addtobag(user,drop,amt)
        if experience:
            desc.append("You gained experience!")
            addtobag(user,"Experience",1)
        if res['abroke0']:
            if amountinbag(user,stats['0'])>0: removefrombag(user,stats['0'])
            else: users[str(user.id)]["equipment"][0] = "None"
            finale += "\nYour weapon {}!".format(break_message(stats['dur0']))
        if res['abroke3']:
            if amountinbag(user,stats['3'])>0: removefrombag(user,stats['3'])
            else: users[str(user.id)]["equipment"][3] = "None"
            finale += "\nYour ammo has been used!"
        if res['abroke1']:
            if amountinbag(user,stats['1'])>0: removefrombag(user,stats['1'])
            else: users[str(user.id)]["equipment"][1] = "None"
            finale += "\nYour armor {}!".format(break_message(stats['dur1']))
        if res['abroke2']:
            if amountinbag(user,stats['2'])>0: removefrombag(user,stats['2'])
            else: users[str(user.id)]["equipment"][2] = "None"
            finale += "\nYour accessory {}!".format(break_message(stats['dur2']))
        users[str(user.id)]["fighttd"] += 1
        #end bits
        users[str(user.id)]["energy"] -= energyuse
        if users[str(user.id)]["energy"] < energyuse: finale += "\nYou have ran out of energy!"
        if 1 + fighttd >= dailylimit: finale += "\nYou have hit the daily fighting limit of {}. Please come again tomorrow.".format(dailylimit)
        writeUsers()
        #display
        desc = "\n".join(desc)
        desc += finale
        em = discord.Embed(title = "Fighting", description = desc, color = colorFighting())
        if item: em.add_field(name=drop,value=amt)
        if experience: em.add_field(name="Experience",value=1)
        await interaction.response.send_message(embed = em)
    
    
    
    
    
    
    ## INFO ##
    
    @app_commands.command(description="Displays info about a mob.")
    @app_commands.describe(mob = "Mob")
    async def mob(self, interaction: discord.Interaction, mob: str):
        try:
            data = getMobs()[format(mob)]
        except:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately that mob could not be found.",color=colorError()))
            return
        pages = [generate_fighting_1(data),generate_fighting_2(data),generate_fighting_3(data)]
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no info could be found.",color=colorError()))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#
    
### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(FightCommands(bot),guilds=[discord.Object(id=490588110590181376)])