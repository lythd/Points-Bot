
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

class ItemCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------COMMANDS----------------------------------------------------------------------------------------#

    ### USERS ###
    
    ## USER INFO COMMANDS ##
    
    @app_commands.command(description="Shows how much energy you have, you can get more by eating food, and you use this to mine.")
    async def energy(self, interaction:discord.Interaction):
        user = interaction.user
        open_account(user)
        users = getUsers()
        
        
        await interaction.response.send_message(embed=discord.Embed(title = "**You have** " + format_number(users[str(user.id)]["energy"]) + " **energy!**",color=colorInfo()))
        
        
        
    @app_commands.command(description="Shows your balance and networth.")
    async def balance(self, interaction:discord.Interaction):
        user = interaction.user
        open_account(user)
        users = getUsers()
        
        amt1 = users[str(user.id)]["money"]
        try:
            amt2 = value_of_items(users[str(user.id)]["bag"])
        except:
            amt2 = 0
        
        em = discord.Embed(title = user.name + "'s Money", color = colorInfo())
        em.add_field(name = "Balance", value = format_number(amt1))
        em.add_field(name = "Bag Value", value = format_number(amt2))
        em.add_field(name = "Net Worth", value = format_number(amt1+amt2))
        await interaction.response.send_message(embed = em)
    
    
        
    @app_commands.command(description="Shows all the items in your bag.")
    async def bag(self, interaction:discord.Interaction):
        user = interaction.user
        open_account(user)
        users = getUsers()
        
        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []
        
        todelete = []
        for i in bag:
            if i['amount'] == 0: todelete.append(i)
        bingo = len(todelete)>0
        for i in todelete: bag.remove(i)
        if bingo: writeUsers()
        
        c=0
        pages = []
        em = discord.Embed(title = "Bag 1/{}".format(math.ceil(len(bag)/21)),color=colorInfo())
        for item in bag:
            name = item["item"]
            amount = item["amount"]
            if amount > 0:
                em.add_field(name = capital(name), value = amount)
            else:
                continue
            c+=1
            if c == 21:
                pages.append(em)
                em = discord.Embed(title = "Bag {}/{}".format(len(pages)+1,math.ceil(len(bag)/21)))
                c=0
            
        if c>0: pages.append(em)
        
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately your bag is empty.",color=colorError()))
    
    
        
    @app_commands.command(description="Shows all the items in your bag following a certain search string.")
    @app_commands.describe(search = "Starts with")
    async def bagsearch(self, interaction:discord.Interaction, search:str=""):
        user = interaction.user
        open_account(user)
        users = getUsers()
        
        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []
        
        todelete = []
        for i in bag:
            if i['amount'] == 0: todelete.append(i)
        bingo = len(todelete)>0
        for i in todelete: bag.remove(i)
        if bingo: writeUsers()
        
        c=0
        pages = []
        em = discord.Embed(title = f"Search for '{search}'",color=colorInfo())
        for item in bag:
            name = item["item"]
            if format(name).startswith(format(search)):
                amount = item["amount"]
                if amount > 0:
                    em.add_field(name = capital(name), value = amount)
                else:
                    continue
                c+=1
                if c == 21:
                    pages.append(em)
                    em = discord.Embed(title = f"Search for '{search}' #{len(pages)+1}",color=colorInfo())
                    c=0
            
        if c>0: pages.append(em)
        
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = f"Nothing found in your bag starting with '{search}'.",color=colorError()))
    
    ## OFFERS/PAYING/LOAN ##
    
    @app_commands.command(description="Once a day you can collect payments from all your loans.")
    async def collectloan(self,interaction:discord.Interaction):
        users = getUsers()
        user = interaction.user
        res = getloans(user.id)
        if res == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**You can only do this once every day.**",color=colorError()))
            return
        if len(res) < 1:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have no outstanding loan payments.**",color=colorError()))
            return
        
        em = discord.Embed(title = "Collected Loan Payments",color=colorTransaction())
        for pair in res:
            users[pair[0]]["money"] -= pair[1]
            users[str(user.id)]["money"] += pair[1]
            em.add_field(name = users[pair[0]]["name"], value = pair[1])
        writeUsers()
        await interaction.response.send_message(embed=em)
    
    @app_commands.command(description="Once a loan request has been sent to you, this command will accept it.")
    async def acceptloan(self,interaction:discord.Interaction):
        global storedloan
        global noneloan
        user = interaction.user
        if storedloan == noneloan:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding loan request. If another loan request has taken place since a loan was requested from you, that loan request might have been erased.**",color=colorError()))
            return
        if user != storedloan[1]:
            await interaction.response.send_message(embed=discord.Embed(title="**You are not the intended recipient of this loan request. If another loan request has taken place since a loan was request from you, that loan request might have been erased.**",color=colorError()))
            return
        bal = update_bank(user)
        if storedloan[2]>bal:
            await interaction.response.send_message(embed=discord.Embed(title="**Insufficient funds, loan cancelled.**",color=colorError()))
            return
        users = getUsers()
        addloan(storedloan[1].id,storedloan[0].id,storedloan[2])
        writeUsers()
        
        update_bank(storedloan[1],-storedloan[2])
        update_bank(storedloan[0],storedloan[2])
        
        await interaction.response.send_message(embed=discord.Embed(title="**You gave a loan of** " + format_number(storedloan[2]) + " **coins.**",color=colorGood()))
        storedloan = noneloan

    @app_commands.command(description="Once a loan request has been sent to you, this command will deny it.")
    async def denyloan(self,interaction:discord.Interaction):
        global storedloan
        global noneloan
        user = interaction.user
        if storedloan == noneloan:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding loan request. If another loan request has taken place since a loan was requested from you, that loan request might have been erased.**",color=colorError()))
            return
        if user != storedloan[1]:
            await interaction.response.send_message(embed=discord.Embed(title="**You are not the intended recipient of this loan request. If another loan request has taken place since a loan was request from you, that loan request might have been erased.**",color=colorError()))
            return
        storedloan = noneloan
        await interaction.response.send_message(embed=discord.Embed(title="**You have denied this loan request.**",color=colorBad()))
        
    @app_commands.command(description="Cancels a loan request you have sent.")
    async def cancelloan(self,interaction:discord.Interaction):
        global storedloan
        global noneloan
        user = interaction.user
        if storedloan == noneloan:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding loan request. If another loan request has taken place since you requested a loan, your loan request might have been erased.**",color=colorError()))
            return
        if user != storedloan[0]:
            await interaction.response.send_message(embed=discord.Embed(title="**You did not send this loan request. If another loan request has taken place since you requested a loan, your loan request might have been erased.**",color=colorError()))
            return
        storedloan = noneloan
        await interaction.response.send_message(embed=discord.Embed(title="**You have cancelled this loan request.**",color=colorBad()))

    @app_commands.command(description="Requests <member> for a loan of <money> coins, they have to type \"/acceptloan\" to accept.")
    @app_commands.describe(member = "Member")
    @app_commands.describe(money = "Money in Loan")
    async def requestloan(self,interaction:discord.Interaction,member:discord.Member,money:int):
        global storedloan
        global noneloan
        user = interaction.user
        if member.bot:
            await interaction.response.send_message(embed=discord.Embed(title="**You cannot ask a bot for a loan.**",color=colorError()))
            return
        open_account(user)
        open_account(member)
        users = getUsers()
        if hasloan(user.id,member.id):
            await interaction.response.send_message(embed=discord.Embed(title=member.name + " **has already given you a loan, that must be paid off first before you can get another loan from them.**",color=colorError()))
            return
        bal = update_bank(member)
        if bal < money:
            await interaction.response.send_message(embed=discord.Embed(title=member.name + " **does not have enough money to lend you a loan of** " + format_number(money) + "**.**",color=colorError()))
            return
        storedloan = [user,member,money]
        await interaction.response.send_message(embed=discord.Embed(title="**You requested** "+member.name+" **for a loan of ** " + format_number(money) + " **coins. You can use /cancelloan to cancel this, and they can use /acceptloan or /denyloan to accept or deny respectively.**",color=colorTransaction()))
    
    @app_commands.command(description="Once an offer has been sent to you, this command will accept it.")
    async def acceptoffer(self,interaction:discord.Interaction):
        global storedoffer
        global noneoffer
        user = interaction.user
        if storedoffer == noneoffer:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outstanding offer. If another offer has taken place since an offer to you was proposed, that offer might have been erased, so ask them to send it again.**",color=colorError()))
            return
        if user != storedoffer[1]:
            await interaction.response.send_message(embed=discord.Embed(title="**You are not the intended recipient of this offer. If another offer has taken place since an offer to you was proposed, that offer might have been erased, so ask them to send it again.**",color=colorError()))
            return
        bal = update_bank(user)
        if storedoffer[4]>bal:
            await interaction.response.send_message(embed=discord.Embed(title="**Insufficient funds, offer cancelled.**",color=colorError()))
            return
        users = getUsers()
        res = removefrombag(storedoffer[0],storedoffer[2],storedoffer[3])
        if res == -1:
            await interaction.response.send_message(embed=discord.Embed(title="**They no longer have enough of this item in their bag.**",color=colorError()))
            return
        addtobag(storedoffer[1],storedoffer[2],storedoffer[3])
        writeUsers()
        
        update_bank(storedoffer[1],-storedoffer[4])
        update_bank(storedoffer[0],storedoffer[4])
        
        await interaction.response.send_message(embed=discord.Embed(title="**You paid** " + format_number(storedoffer[4]) + " **coins for** " + format_number(storedoffer[3]) + " " + storedoffer[2] + "**.**",color=colorGood()))
        storedoffer = noneoffer

    @app_commands.command(description="Once an offer has been sent to you, this command will deny it.")
    async def denyoffer(self,interaction:discord.Interaction):
        global storedoffer
        global noneoffer
        user = interaction.user
        if storedoffer == noneoffer:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding offer. If another offer has taken place since an offer to you was proposed, that offer might have been erased.**",color=colorError()))
            return
        if user != storedoffer[1]:
            await interaction.response.send_message(embed=discord.Embed(title="**You are not the intended recipient of this offer. If another offer has taken place since an offer to you was proposed, that offer might have been erased.**",color=colorError()))
            return
        storedoffer = noneoffer
        await interaction.response.send_message(embed=discord.Embed(title="**You have denied this offer.**",color=colorBad))
        
    @app_commands.command(description="Cancels an offer you have sent.")
    async def canceloffer(self,interaction:discord.Interaction):
        global storedoffer
        global noneoffer
        user = interaction.user
        if storedoffer == noneoffer:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding offer. If another offer has taken place since your offer, your offer might have been erased.**",color=colorError()))
            return
        if user != storedoffer[0]:
            await interaction.response.send_message(embed=discord.Embed(title="**You did not send this offer. If another offer has taken place since your offer, your offer might have been erased.**",color=colorError()))
            return
        storedoffer = noneoffer
        await interaction.response.send_message(embed=discord.Embed(title="**You have cancelled this offer.**",color=colorBad()))

    @app_commands.command(description="Offers <amt> of <item> to <member> for <price>, they have to type \"/acceptoffer\" to accept.")
    @app_commands.describe(member = "Member")
    @app_commands.describe(price = "Total Price")
    @app_commands.describe(item = "Item")
    @app_commands.describe(amt = "Amount")
    async def offer(self,interaction:discord.Interaction,member:discord.Member,price:int,item:str,amt:int=1):
        global storedoffer
        global noneoffer
        user = interaction.user
        if member.bot:
            await interaction.response.send_message(embed=discord.Embed(title="**You cannot make an offer to a bot.**",color=colorError()))
            return
        if not (valid_item(item)):
            await interaction.response.send_message(embed=discord.Embed(title="**Invalid item.**",color=colorError()))
            return
        open_account(user)
        open_account(member)
        users = getUsers()
        if removefrombag(user,item,amt) == -1:
            await interaction.response.send_message(embed=discord.Embed(title="**You do not have enough of this item.**",color=colorError()))
            return
        storedoffer = [user,member,item,amt,price]
        await interaction.response.send_message(embed=discord.Embed(title="**You have made an offer to** "+member.name+" **of** " + format_number(amt) + " " + item + " **for** " + format_number(price) + " **coins. You can use /canceloffer to cancel this, and they can use /acceptoffer or /denyoffer to accept or deny respectively.**",color=colorTransaction()))
        
    @app_commands.command(description="Pays money to a person.")
    @app_commands.describe(member = "Member")
    @app_commands.describe(amount = "Amount")
    async def pay(self,interaction:discord.Interaction,member:discord.Member,amount:int):
        if member.bot:
            await interaction.response.send_message(embed=discord.Embed(title="**You cannot pay a bot.**",color=colorError()))
            return
        user = interaction.user
        open_account(user)
        open_account(member)
        
        if amount == None:
            await interaction.response.send_message(embed=discord.Embed(title="**No amount entered, transaction cancelled.**",color=colorError()))
            return
        
        bal = update_bank(user)
        
        amount = int(amount)
        if amount>bal:
            await interaction.response.send_message(embed=discord.Embed(title="**Insufficient funds, transaction cancelled.**",color=colorError()))
            return
        if amount<0:
            await interaction.response.send_message(embed=discord.Embed(title="**Amount must be positive, transaction cancelled.**",color=colorError()))
            return
        
        update_bank(user,-amount)
        update_bank(member,amount)
        
        await interaction.response.send_message(embed=discord.Embed(title="**You paid** " + format_number(amount) + " **coins to** "+member.name+"**!**",color=colorTransaction()))
    
    
    
    
    ## BASIC MONEY/ITEM COMMANDS ##
    
    
    @app_commands.command(description="Consumes an item to get more energy.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(amount = "Amount")
    async def consume(self,interaction:discord.Interaction,item:str,amount:int = 1):
        user = interaction.user
        open_account(user)
        
        res = consume_this(user,item,amount)
        
        if res[0] > 0:
            if res[0] == 1:
                await interaction.response.send_message(embed=discord.Embed(title="**That Object isn't there!**",color=colorError()))
                return
            if res[0] == 2:
                await interaction.response.send_message(embed=discord.Embed(title=item + " **is not able to be consumed!**",color=colorError()))
                return
            if res[0] == 3:
                await interaction.response.send_message(embed=discord.Embed(title="**You don't have** " + format_number(amount) + " " + item + " **in your bag.**",color=colorError()))
                return
            if res[0] == 4:
                await interaction.response.send_message(embed=discord.Embed(title="**You don't have** " + item + " **in your bag.**",color=colorError()))
                return
            
        await interaction.response.send_message(embed=discord.Embed(title="**You just ate** " + format_number(amount) + " " + item + " **for** " + format_number(res[1]) + " **energy{}.**".format(", that wasn't very pleasant" if res[1] < 0 else ""),color=colorInfo()))
        
    @app_commands.command(description="Bets money on a coinflip, if it lands on heads you win the amount, if it lands on tails you lose it.")
    @app_commands.describe(amount = "Amount")
    async def coinflip(self,interaction:discord.Interaction,amount:int):
        user = interaction.user
        open_account(user)
        
        bal = update_bank(user)
        
        amount = int(amount)
        if amount>bal:
            await interaction.response.send_message(embed=discord.Embed(title = "**Insufficient funds, coinflip cancelled.**",color=colorError()))
            return
        if amount<0:
            await interaction.response.send_message(embed=discord.Embed(title = "**Amount must be positive, coinflip cancelled.**",color=colorError()))
            return
        
        a = random.choice(["Heads","Tails"])
                           
        if a == "Heads":
            await interaction.response.send_message(embed=discord.Embed(title = "**The coin landed on heads\nYou won** " + format_number(amount),color=colorGood()))
            update_bank(user,amount)
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**The coin landed on tails\nYou paid** " + format_number(amount),color=colorBad()))
            update_bank(user,-amount)
    
    @app_commands.command(description="Some random betting thing no idea how it works anymore.")
    @app_commands.describe(amount = "Amount")
    async def slots(self,interaction:discord.Interaction,amount:int):
        user = interaction.user
        open_account(user)
        if amount == None:
            await interaction.response.send_message(embed=discord.Embed(title = "**No amount entered, slots cancelled.**",color=colorError()))
            return
        
        bal = update_bank(user)
        
        amount = int(amount)
        if amount>bal:
            await interaction.response.send_message(embed=discord.Embed(title = "**Insufficient funds, slots cancelled.**",color=colorError()))
            return
        if amount<1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Amount must be at least 1, slots cancelled.**",color=colorError()))
            return
        
        msg = "**You paid** " + format_number(amount) + "\n"
        update_bank(user,-amount)
        
        final = []
        for i in range(3):
            a = random.choice(['X','O','Q','$'])
            
            final.append(a)
        
        msg += str(final) + "\n"
        
        if '$' == final[0] == final[1] == final[2]:
            update_bank(user,20*amount)
            await interaction.response.send_message(embed=discord.Embed(title = msg + "**You won** " + format_number(20*amount) +"**!**",color=colorGood()))
        elif final[0] == final[1] == final[2]:
            update_bank(user,10*amount)
            await interaction.response.send_message(embed=discord.Embed(title = msg + "**You won** " + format_number(10*amount) +"**!**",color=colorGood()))
        else:
            pity = 0
            if final[0] == '$':
                pity += 1
            if final[1] == '$':
                pity += 1
            if final[2] == '$':
                pity += 1
            if pity > 1:
                update_bank(user,round(1.5*amount))
                await interaction.response.send_message(embed=discord.Embed(title = msg + "**You won** " + format_number(round(1.5*amount)) + "**!**",color=colorGood()))
            elif pity > 0:
                update_bank(user,10)
                await interaction.response.send_message(embed=discord.Embed(title = msg + "**You won** 10**!**",color=colorBad()))
            else:
                if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
                    update_bank(user,round(0.1*amount))
                    await interaction.response.send_message(embed=discord.Embed(title = msg + "**You won** " + format_number(round(0.1*amount)) + "**!**",color=colorBad()))
                else:
                    await interaction.response.send_message(embed=discord.Embed(title = msg + "**You didn't win.**",color=colorBad()))
    
    @app_commands.command(description="Gets between 1 and 100 coins, can be used every day.")
    async def beg(self, interaction:discord.Interaction):
        user = interaction.user
        open_account(user)
        earnings = beg_this(user)
        if earnings == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**You can only do this once every day.**",color=colorError()))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**Someone gave you** " + format_number(earnings) + " **coins!!**",color=colorGood()))
        
    
    @app_commands.command(description="Buys a specified amount of an item from the shop.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(amount = "Amount")
    async def buy(self, interaction,item:str,amount:int=1):
        user = interaction.user
        open_account(user)
        
        res = buy_this(user,item,amount)
        
        if res[0]>0:
            if res[0]==1:
                await interaction.response.send_message(embed=discord.Embed(title = "**That Object isn't there!**",color=colorError()))
                return
            if res[0]==2:
                await interaction.response.send_message(embed=discord.Embed(title = format_number(amount) + " " + item + " **is unavailable.**",color=colorError()))
                return
            if res[0]==3:
                await interaction.response.send_message(embed=discord.Embed(title = "**You don't have enough money in your wallet to buy** " + format_number(amount) + " **of** " + item,color=colorError()))
                return
            if res[0]==4:
                await interaction.response.send_message(embed=discord.Embed(title = "**This item is not available on the market.**",color=colorError()))
                return
        
        
        await interaction.response.send_message(embed=discord.Embed(title = "**You just bought** " + format_number(amount) + " " + item + " **for** " + format_number(res[1]) + " **coins.**",color=colorTransaction()))
    
    
    @app_commands.command(description="Sells a specified amount of an item back to the shop. 90% Refund Rate.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(amount = "Amount")
    async def sell(self, interaction,item:str,amount:int = 1):
        user = interaction.user
        open_account(user)
        
        res = sell_this(user,item,amount)
        
        if res[0] > 0:
            if res[0] == 1:
                await interaction.response.send_message(embed=discord.Embed(title = "**That Object isn't there!**",color=colorError()))
                return
            if res[0] == 2:
                await interaction.response.send_message(embed=discord.Embed(title = "**You don't have** " + format_number(amount) + " " + item + " **in your bag.**",color=colorError()))
                return
            if res[0] == 3:
                await interaction.response.send_message(embed=discord.Embed(title = "**You don't have** " + item + " **in your bag.**",color=colorError()))
                return
            if res[0] == 4:
                await interaction.response.send_message(embed=discord.Embed(title = "**This item is not available on the market.**",color=colorError()))
                return
        
        await interaction.response.send_message(embed=discord.Embed(title = "**You just sold** " + format_number(amount) + " " + item + " **for** " + format_number(res[1]) + " **coins.**",color=colorTransaction()))
        

    @app_commands.command(description="Shows, buys, or sells the daily item.")
    @app_commands.choices(mode = [
        Choice(name="Show",value="show"),
        Choice(name="Buy",value="buy"),
        Choice(name="Sell",value="sell")
    ])
    @app_commands.describe(mode = "Mode")
    @app_commands.describe(amount = "Amount")
    async def daily(self,interaction:discord.Interaction,mode:typing.Optional[str]="show",amount:int=1):
        user = interaction.user
        item = get_daily_item()
        cost = item[1] * amount
        if mode == "buy":
            open_account(user)
            users = getUsers()
            bal = update_bank(user)
            if bal < cost:
                await interaction.response.send_message(embed=discord.Embed(title = "**You cannot afford this, you need** " + format_number(cost) + "**.**",color=colorError()))
                return
            users = addtobag(user,item[0],amount)
        
            writeUsers()
            
            update_bank(user,-cost)
            await interaction.response.send_message(embed=discord.Embed(title = "**You have bought** " + format_number(amount) + " " + item[0] + " **for** " + format_number(cost) + " **coins.**",color=colorTransaction()))
            return
        if mode == "sell":
            cost = math.floor(cost*0.9)
            open_account(user)
            users = getUsers()
            bal = update_bank(user)
            res = removefrombag(user,item[0],amount)
            if res == -1:
                await interaction.response.send_message(embed=discord.Embed(title = "**You do not have this many.**",color=colorError()))
                return
        
            writeUsers()
            
            update_bank(user,cost)
            await interaction.response.send_message(embed=discord.Embed(title = "**You have sold** " + format_number(amount) + " " + item[0] + " **for** " + format_number(cost) + " **coins.**",color=colorTransaction()))
            return
        await interaction.response.send_message(embed=discord.Embed(title = "**The daily item is** " + item[0] + " **and it costs** " + format_number(cost) + "**.**",color=colorShop()))
        return

    
    @app_commands.command(description="Crafts a specified amount of an item, check /recipes for the recipes.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(amount = "Amount")
    async def craft(self,interaction:discord.Interaction,item:str,amount:int = 1):
        user = interaction.user
        open_account(user)
        users = getUsers()
        
        if amount < 1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Crafting failed, amount must be positive.**",color=colorError()))
            return
        
        recipe = getCrafting()[format(item)]
        inputs = {i:a*amount for i,a in recipe['inputs'].items()}
        amt = amount * recipe['amount']
        
        for i,a in inputs.items():
            if amountinbag(user,i) < a:
                await interaction.response.send_message(embed=discord.Embed(title = "**You cannot afford this, you need** {} **of** {}**, you only have** {}**.**".format(a,capital(i),amountinbag(user,i)),color=colorError()))
                return
        removeallfrombag(user,inputs)
        addtobag(user,format(item),amt)
        
        await interaction.response.send_message(embed=discord.Embed(title = "**You have crafted** " + format_number(amt) + " **of** " + capital(item) + "**.**",color=colorCrafting()))

    
    @app_commands.command(description="Brews a specified amount of a potion, check /potions for the recipes.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(amount = "Amount")
    async def brew(self,interaction:discord.Interaction,item:str,amount:int = 1):
        user = interaction.user
        open_account(user)
        users = getUsers()
        
        if amount < 1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Brewing failed, amount must be positive.**",color=colorError()))
            return
        
        recipe = getBrewing()[format(item)]
        inputs = {i:a*amount for i,a in recipe['inputs'].items()}
        amt = amount * recipe['amount']
        
        for i,a in inputs.items():
            if amountinbag(user,i) < a:
                await interaction.response.send_message(embed=discord.Embed(title = "**You cannot afford this, you need** {} **of** {}**, you only have** {}**.**".format(a,capital(i),amountinbag(user,i)),color=colorError()))
                return
        removeallfrombag(user,inputs)
        addtobag(user,format(item),amt)
        
        await interaction.response.send_message(embed=discord.Embed(title = "**You have brewed** " + format_number(amt) + " **of** " + capital(item) + "**.**",color=colorCrafting()))
        


    ### ITEMS ###

    @app_commands.command(name = "item", description = "Views the price and description of a particular item")
    @app_commands.describe(item = "Item")
    async def item(self, interaction: discord.Interaction, item: str):
        effects = []
        #generic
        category = get_item_category(item)
        price = get_item_price(item)
        description = get_item_desc(item)
        #food
        fenergy = get_food_energy(item)
        #pickaxe
        ptier = get_pickaxe_tier(item)
        pdoc = get_pickaxe_doc(item)
        pdur = get_pickaxe_dur(item)
        #rod
        rfp = get_rod_fp(item)
        rlbc = get_rod_lbc(item)
        rbcc = get_rod_bcc(item)
        rdur = get_rod_dur(item)
        #weapon
        wpdmg = get_weapon_pdmg(item)
        wbdmg = get_weapon_bdmg(item)
        wdur = get_weapon_dur(item)
        effects += get_weapon_effects(item)
        #armor
        adef = get_armor_def(item)
        adur = get_armor_dur(item)
        effects += get_armor_effects(item)
        #accessory
        cdur = get_accessory_dur(item)
        effects += get_accessory_effects(item)
        #ammo
        mpdmg = get_ammo_pdmg(item)
        mbdmg = get_ammo_bdmg(item)
        effects += get_ammo_effects(item)
        #bait
        bfp = get_bait_fp(item)
        bdrop = get_bait_drop(item)
        effects += get_bait_effects(item)
        #embed
        em = discord.Embed(title = f"{capital(item)} Info", color = colorInfo())
        if category == -1:
            category = "Item not found!"
        if price == -1:
            price = "???"
        if description == -1:
            description = "Item not found!"
        em.add_field(name = "Price", value = format_number(price))
        for var,name in [(fenergy,"Energy"),(ptier,"Mining Tier"),(pdoc,"Double Ore Chance"),(pdur,"Durability"),(rfp,"Fishing Power"),(rlbc,"Line Break Chance"),(rbcc,"Bait Consumption Chance"),(rdur,"Durability"),(wpdmg,"Piercing Damage"),(wbdmg,"Blunt Damage"),(wdur,"Durability"),(adef,"Defense"),(adur,"Durability"),(cdur,"Durability"),(mpdmg,"Piercing Damage"),(mbdmg,"Blunt Damage"),(bfp,"Fishing Power")]:
            if var != -1: em.add_field(name = name, value = format_number(var))
        for var,name in [(bdrop,"Special Drop")]:
            if var != 'None': em.add_field(name = name, value = capital(var))
        for effect in effects:
            em.add_field(name = effect, value = get_effect_description(effect))
        em.add_field(name = "Category", value = capital(category))
        em.add_field(name = "Description", value = description)
        await interaction.response.send_message(embed = em)
    
    
    
    
    
    @app_commands.command(name = "additem", description = "Just for ly ;)")
    @app_commands.choices(category = [Choice(name=n,value=v) for n,v in get_categories()])
    @app_commands.describe(item_name = "Item Name")
    @app_commands.describe(category = "Category")
    @app_commands.describe(description = "Description")
    @app_commands.describe(starting_price = "Starting Price")
    @app_commands.describe(starting_amount = "Starting Amount")
    @app_commands.describe(energy = "Energy")
    async def add_item(self, interaction: discord.Interaction, item_name: str, starting_price:int, starting_amount:int, category: typing.Optional[str] = "generic", description: typing.Optional[str] = "", energy:typing.Optional[int]=0):
        if interaction.user.id == 325691401851633674:
            item_add(capital(item_name),description,format(category),starting_price,starting_amount,energy)
            await interaction.response.send_message("Added that item", ephemeral = True)
        else:
            await interaction.response.send_message("You are not ly ;)", ephemeral = True)





    @app_commands.command(name = "shop", description = "Shows all the items in the shop. Can specify a category, or use All.")
    @app_commands.choices(category = [Choice(name="All",value="all")]+[Choice(name=n,value=v) for n,v in get_categories()])
    @app_commands.describe(category = "Category")
    async def shop(self, interaction: discord.Interaction, category: typing.Optional[str] = "all"):
        pages = []
        items = copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        while lensorteditems<target:
            name=""
            item_=None
            price=-100
            nonmarkets=[]
            for item in items:
                name=item['name']
                if market_item_of(item):
                    newprice=get_item_price_of(item)
                    if newprice>=price and not (name in item_names):
                        item_=item
                        price=newprice
                else:
                    target-=1
                    nonmarkets.append(item)
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['price']>0 and (category == "all" or item_['category'] in category.split(',')): sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
            for non in nonmarkets:
                items.remove(non)
        em = discord.Embed(title = "Market{} 1/{}".format("" if category == "all" else " {}".format(capital(category)), math.ceil(len(sorted_items)/18)),color=colorShop())
        for item in sorted_items:
            name = item['name']
            price = get_item_price(format(name))
            start = format_number(price)
            if price < 0:
                start = "Unavailable"
            elif price < 1:
                start = "1"
            desc = item["description"]
            em.add_field(name = name, value = start + "c | " + desc)
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Market{} {}/{}".format("" if category == "all" else " {}".format(capital(category)), len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorShop())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))

    @app_commands.command(name = "itemlist", description = "Shows all the items. Can specify a category, or use All.")
    @app_commands.choices(category = [Choice(name="All",value="all")]+[Choice(name=n,value=v) for n,v in get_categories()])
    @app_commands.describe(category = "Category")
    async def itemlist(self, interaction: discord.Interaction, category: typing.Optional[str] = "all"):
        pages = []
        items =  copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        while lensorteditems<target:
            name_=""
            name=""
            item_=None
            for item in items:
                name=item['name']
                if (name_=="" or format(name) < format(name_)) and not (name in item_names):
                    item_=item
                    name_=name
            if not (item_ is None):
                item_names.append(item_['name'])
                if category == "all" or item_['category'] in category.split(','): sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
        em = discord.Embed(title = "Item List{} 1/{}".format("" if category == "all" else " {}".format(capital(category)), math.ceil(len(sorted_items)/18)),color=colorInfo())
        for item in sorted_items:
            name = item['name']
            price = get_item_price(format(name))
            desc = item["description"]
            em.add_field(name = name, value = desc)
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Item List{} {}/{}".format("" if category == "all" else " {}".format(capital(category)), len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))










    @app_commands.command(name = "shortshop", description = "Shows all the items in the shop. Can specify a category, or use All.")
    @app_commands.choices(category = [Choice(name="All",value="all")]+[Choice(name=n,value=v) for n,v in get_categories()])
    @app_commands.describe(category = "Category")
    async def shortshop(self, interaction: discord.Interaction, category: typing.Optional[str] = "all"):
        pages = []
        items = copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        while lensorteditems<target:
            name=""
            item_=None
            price=-100
            nonmarkets=[]
            for item in items:
                name=item['name']
                if market_item_of(item):
                    newprice=get_item_price_of(item)
                    if newprice>=price and not (name in item_names):
                        item_=item
                        price=newprice
                else:
                    target-=1
                    nonmarkets.append(item)
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['price']>0 and (category == "all" or item_['category'] in category.split(',')): sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
            for non in nonmarkets:
                items.remove(non)
        em = discord.Embed(title = "Market{} 1/{}".format("" if category == "all" else " {}".format(capital(category)), math.ceil(len(sorted_items)/18)),color=colorShop())
        for item in sorted_items:
            name = item['name']
            price = get_item_price(format(name))
            start = format_number(price)
            if price < 0:
                start = "Unavailable"
            elif price < 1:
                start = "1"
            desc = item["description"]
            em.add_field(name = name, value = start + "c")
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Market{} {}/{}".format("" if category == "all" else " {}".format(capital(category)), len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorShop())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))
    
    



    
    @app_commands.command(description="Shows all the duel items.")
    @app_commands.choices(mode = [
        Choice(name="Current Duel Items",value=1),
        Choice(name="Any Duel Items",value=2),
        Choice(name="No Overpowered Items",value=3),
        Choice(name="No Godly Items",value=4),
        Choice(name="Anything Goes",value=5)
    ])
    @app_commands.choices(category = [
        Choice(name="All",value=-1),
        Choice(name="Weapons",value=0),
        Choice(name="Armor",value=1),
        Choice(name="Accessories",value=2),
        Choice(name="Ammo",value=3)
    ])
    @app_commands.describe(mode = "Mode")
    @app_commands.describe(category = "Category")
    async def duelitems(self, interaction: discord.Interaction, mode:typing.Optional[int]=1, category:typing.Optional[int]=-1):
        pages = []
        items =  copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        dict = {x:y for x,y in get_categories()}
        while lensorteditems<target:
            name_=""
            name=""
            item_=None
            for item in items:
                name=item['name']
                if (name_=="" or format(name) < format(name_)) and not (name in item_names):
                    item_=item
                    name_=name
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['category'] in dict['Weapons'].split(',') and category in [-1,0]:
                    if weaponsuitability(item_['name']) < mode: sorted_items.append(item_)
                elif item_['category'] in dict['Armor'].split(',') and category in [-1,1]:
                    if armorsuitability(item_['name']) < mode: sorted_items.append(item_)
                elif item_['category'] in dict['Accessories'].split(',') and category in [-1,2]:
                    if accessorysuitability(item_['name']) < mode: sorted_items.append(item_)
                elif item_['category'] in dict['Ammo'].split(',') and category in [-1,3]:
                    if ammosuitability(item_['name']) < mode: sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
        em = discord.Embed(title = "Duel Items List 1/{}".format(math.ceil(len(sorted_items)/18)),color=colorInfo())
        for item in sorted_items:
            name = item['name']
            price = get_item_price(format(name))
            desc = item["description"]
            em.add_field(name = name, value = "")
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Duel Items List {}/{}".format(len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))
    



    
    @app_commands.command(description="Shows all the weapons.")
    @app_commands.choices(mode = [
        Choice(name="Current Duel Items",value=1),
        Choice(name="Any Duel Items",value=2),
        Choice(name="No Overpowered Items",value=3),
        Choice(name="No Godly Items",value=4),
        Choice(name="Anything Goes",value=5)
    ])
    @app_commands.describe(mode = "Mode")
    async def weaponlist(self, interaction: discord.Interaction, mode:typing.Optional[int]=5):
        pages = []
        items =  copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        dict = {x:y for x,y in get_categories()}
        while lensorteditems<target:
            cst_=-1
            name=""
            item_=None
            for item in items:
                name=item['name']
                cst=0
                if (tst := get_weapon_pdmg(name)) > 0 : cst += tst
                if (tst := get_weapon_bdmg(name)) > 0 : cst += tst
                if (cst_==-1 or cst > cst_) and not (name in item_names):
                    item_=item
                    cst_ = cst
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['category'] in dict['Weapons'].split(','):
                    if weaponsuitability(item_['name']) < mode: sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
        em = discord.Embed(title = "Weapons List 1/{}".format(math.ceil(len(sorted_items)/18)),color=colorInfo())
        for item in sorted_items:
            name = item['name']
            val = []
            if (tst := get_weapon_pdmg(name)) > 0 : val.append(f"{tst}p")
            if (tst := get_weapon_bdmg(name)) > 0 : val.append(f"{tst}b")
            if (tst := get_weapon_dur(name)) > 0 : val.append(f"{tst} dur")
            val += get_weapon_effects(name)
            em.add_field(name = name, value = " | ".join(val))
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Weapons List {}/{}".format(len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))
    



    
    @app_commands.command(description="Shows all the pickaxes. Use /tiers to see what each tier can mine.")
    @app_commands.choices(mode = [
        Choice(name="Current Duel Items",value=1),
        Choice(name="Any Duel Items",value=2),
        Choice(name="No Overpowered Items",value=3),
        Choice(name="No Godly Items",value=4),
        Choice(name="Anything Goes",value=5)
    ])
    @app_commands.describe(mode = "Mode")
    async def pickaxelist(self, interaction: discord.Interaction, mode:typing.Optional[int]=5):
        pages = []
        items =  copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        dict = {x:y for x,y in get_categories()}
        while lensorteditems<target:
            cst_=-1
            name=""
            item_=None
            for item in items:
                name=item['name']
                cst=0
                if (tst := get_pickaxe_tier(name)) > 0 : cst += tst*100
                if (tst := get_pickaxe_doc(name)) > 0 : cst += tst
                if (cst_==-1 or cst > cst_) and not (name in item_names):
                    item_=item
                    cst_ = cst
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['category'] in dict['Pickaxes'].split(','):
                    if weaponsuitability(item_['name']) < mode: sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
        em = discord.Embed(title = "Pickaxes List 1/{}".format(math.ceil(len(sorted_items)/18)),color=colorInfo())
        for item in sorted_items:
            name = item['name']
            val = []
            if (tst := get_pickaxe_tier(name)) > 0 : val.append(f"Tier {tst}")
            if (tst := get_pickaxe_doc(name)) > 0 : val.append(f"{tst}% doc")
            if (tst := get_pickaxe_dur(name)) > 0 : val.append(f"{tst} dur")
            em.add_field(name = name, value = " | ".join(val))
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Pickaxes List {}/{}".format(len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))
    



    
    @app_commands.command(description="Shows all the fishing rods.")
    @app_commands.choices(mode = [
        Choice(name="Current Duel Items",value=1),
        Choice(name="Any Duel Items",value=2),
        Choice(name="No Overpowered Items",value=3),
        Choice(name="No Godly Items",value=4),
        Choice(name="Anything Goes",value=5)
    ])
    @app_commands.describe(mode = "Mode")
    async def rodlist(self, interaction: discord.Interaction, mode:typing.Optional[int]=5):
        pages = []
        items =  copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        dict = {x:y for x,y in get_categories()}
        while lensorteditems<target:
            cst_=-1
            name=""
            item_=None
            for item in items:
                name=item['name']
                cst=0
                if (tst := get_rod_fp(name)) > 0 : cst += tst
                if (cst_==-1 or cst > cst_) and not (name in item_names):
                    item_=item
                    cst_ = cst
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['category'] in dict['Fishing Rods'].split(','):
                    if weaponsuitability(item_['name']) < mode: sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
        em = discord.Embed(title = "Rods List 1/{}".format(math.ceil(len(sorted_items)/18)),color=colorInfo())
        for item in sorted_items:
            name = item['name']
            val = []
            if (tst := get_rod_fp(name)) > 0 : val.append(f"{tst} fp")
            if (tst := get_rod_lbc(name)) > 0 : val.append(f"{tst}% lbc")
            if (tst := get_rod_bcc(name)) > 0 : val.append(f"{tst}% bcc")
            if (tst := get_rod_dur(name)) > 0 : val.append(f"{tst} dur")
            em.add_field(name = name, value = " | ".join(val))
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Rods List {}/{}".format(len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))
    



    
    @app_commands.command(description="Shows all the armor.")
    @app_commands.choices(mode = [
        Choice(name="Current Duel Items",value=1),
        Choice(name="Any Duel Items",value=2),
        Choice(name="No Overpowered Items",value=3),
        Choice(name="No Godly Items",value=4),
        Choice(name="Anything Goes",value=5)
    ])
    @app_commands.describe(mode = "Mode")
    async def armorlist(self, interaction: discord.Interaction, mode:typing.Optional[int]=5):
        pages = []
        items =  copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        dict = {x:y for x,y in get_categories()}
        while lensorteditems<target:
            cst_=-1
            name=""
            item_=None
            for item in items:
                name=item['name']
                cst=0
                if (tst := get_armor_def(name)) > 0 : cst += tst
                if (cst_==-1 or cst > cst_) and not (name in item_names):
                    item_=item
                    cst_ = cst
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['category'] in dict['Armor'].split(','):
                    if armorsuitability(item_['name']) < mode: sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
        em = discord.Embed(title = "Armor List 1/{}".format(math.ceil(len(sorted_items)/18)),color=colorInfo())
        for item in sorted_items:
            name = item['name']
            val = []
            if (tst := get_armor_def(name)) > 0 : val.append(f"{tst}d")
            if (tst := get_armor_dur(name)) > 0 : val.append(f"{tst} dur")
            val += get_armor_effects(name)
            em.add_field(name = name, value = " | ".join(val))
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Armor List {}/{}".format(len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))
    



    
    @app_commands.command(description="Shows all the accessories.")
    @app_commands.choices(mode = [
        Choice(name="Current Duel Items",value=1),
        Choice(name="Any Duel Items",value=2),
        Choice(name="No Overpowered Items",value=3),
        Choice(name="No Godly Items",value=4),
        Choice(name="Anything Goes",value=5)
    ])
    @app_commands.describe(mode = "Mode")
    async def accessorylist(self, interaction: discord.Interaction, mode:typing.Optional[int]=5):
        pages = []
        items =  copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        dict = {x:y for x,y in get_categories()}
        while lensorteditems<target:
            cst_=-1
            name=""
            item_=None
            for item in items:
                name=item['name']
                cst=0
                if (tst := get_accessory_dur(name)) > 0 : cst += tst
                if (cst_==-1 or cst > cst_) and not (name in item_names):
                    item_=item
                    cst_ = cst
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['category'] in dict['Accessories'].split(','):
                    if accessorysuitability(item_['name']) < mode: sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
        em = discord.Embed(title = "Accessory List 1/{}".format(math.ceil(len(sorted_items)/18)),color=colorInfo())
        for item in sorted_items:
            name = item['name']
            val = []
            if (tst := get_accessory_dur(name)) > 0 : val.append(f"{tst} dur")
            val += get_accessory_effects(name)
            em.add_field(name = name, value = " | ".join(val))
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Accessory List {}/{}".format(len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))
    



    
    @app_commands.command(description="Shows all the ammunition.")
    @app_commands.choices(mode = [
        Choice(name="Current Duel Items",value=1),
        Choice(name="Any Duel Items",value=2),
        Choice(name="No Overpowered Items",value=3),
        Choice(name="No Godly Items",value=4),
        Choice(name="Anything Goes",value=5)
    ])
    @app_commands.describe(mode = "Mode")
    async def ammolist(self, interaction: discord.Interaction, mode:typing.Optional[int]=5):
        pages = []
        items =  copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        dict = {x:y for x,y in get_categories()}
        while lensorteditems<target:
            cst_=-1
            name=""
            item_=None
            for item in items:
                name=item['name']
                cst=0
                if (tst := get_ammo_pdmg(name)) > 0 : cst += tst
                if (tst := get_ammo_bdmg(name)) > 0 : cst += tst
                if (cst_==-1 or cst > cst_) and not (name in item_names):
                    item_=item
                    cst_ = cst
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['category'] in dict['Ammo'].split(','):
                    if ammosuitability(item_['name']) < mode: sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
        em = discord.Embed(title = "Ammo List 1/{}".format(math.ceil(len(sorted_items)/18)),color=colorInfo())
        for item in sorted_items:
            name = item['name']
            val = []
            if (tst := get_ammo_pdmg(name)) > 0 : val.append(f"{tst}p")
            if (tst := get_ammo_bdmg(name)) > 0 : val.append(f"{tst}b")
            val += get_ammo_effects(name)
            em.add_field(name = name, value = " | ".join(val))
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Ammo List {}/{}".format(len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))
    



    
    @app_commands.command(description="Shows all the bait.")
    @app_commands.choices(mode = [
        Choice(name="Current Duel Items",value=1),
        Choice(name="Any Duel Items",value=2),
        Choice(name="No Overpowered Items",value=3),
        Choice(name="No Godly Items",value=4),
        Choice(name="Anything Goes",value=5)
    ])
    @app_commands.describe(mode = "Mode")
    async def baitlist(self, interaction: discord.Interaction, mode:typing.Optional[int]=5):
        pages = []
        items =  copy.deepcopy(getItems())
        count = 0
        sorted_items = []
        item_names = []
        target=len(items)
        lensorteditems = 0
        dict = {x:y for x,y in get_categories()}
        while lensorteditems<target:
            cst_=-1
            name=""
            item_=None
            for item in items:
                name=item['name']
                cst=0
                if (tst := get_bait_fp(name)) > 0 : cst += tst
                if get_bait_drop(name) != 'None' : cst += 0.5
                if (cst_==-1 or cst > cst_) and not (name in item_names):
                    item_=item
                    cst_ = cst
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['category'] in dict['Bait'].split(','):
                    if ammosuitability(item_['name']) < mode: sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
        em = discord.Embed(title = "Bait List 1/{}".format(math.ceil(len(sorted_items)/18)),color=colorInfo())
        for item in sorted_items:
            name = item['name']
            val = []
            if (tst := get_bait_fp(name)) > 0 : val.append(f"{tst} fp")
            if (tst := get_bait_drop(name)) != "None" : val.append(f"Drops {tst}")
            val += get_bait_effects(name)
            em.add_field(name = name, value = " | ".join(val))
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Bait List {}/{}".format(len(pages)+1, math.ceil(len(sorted_items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))




    
    
    @app_commands.command(description="Shows all of the crafting recipes.")
    @app_commands.choices(category = [Choice(name="All",value="all")]+[Choice(name=n,value=v) for n,v in get_categories()])
    @app_commands.describe(category = "Category")
    async def recipes(self, interaction: discord.Interaction, category: typing.Optional[str] = "all"):
        items = []
        for name,data in getCrafting().items():
            if category == "all" or data['category'] in category.split(','):
                value = "Amount: {}\n".format(data['amount'])
                value += ", ".join([f"{a} {capital(i)}" for i,a in data['inputs'].items()])
                items.append((capital(name), value))
        count = 0
        pages = []
        em = discord.Embed(title = "Crafting{} 1/{}".format("" if category == "all" else " {}".format(capital(category)), math.ceil(len(items)/18)),color=colorInfo())
        for name,value in items:
            em.add_field(name=name,value=value)
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Crafting{} {}/{}".format("" if category == "all" else " {}".format(capital(category)), len(pages)+1, math.ceil(len(items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=colorError()))
    
    
    
    
    
    @app_commands.command(description="Shows all of the brewing recipes.")
    async def potions(self, interaction: discord.Interaction):
        items = []
        for name,data in getBrewing().items():
            value = "Amount: {}\n".format(data['amount'])
            value += ", ".join([f"{a} {capital(i)}" for i,a in data['inputs'].items()])
            items.append((capital(name), value))
        count = 0
        pages = []
        em = discord.Embed(title = "Brewing 1/{}".format(math.ceil(len(items)/18)),color=colorInfo())
        for name,value in items:
            em.add_field(name=name,value=value)
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Brewing {}/{}".format(len(pages)+1, math.ceil(len(items)/18)),color=colorInfo())
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(ItemCommands(bot),guilds=[discord.Object(id=490588110590181376)])