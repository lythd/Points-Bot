
#---------------------------------------------------------------------------SETUP----------------------------------------------------------------------------------------#

### IMPORTS ###

## DISCORD ##
import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

## MY OWN ##
from ButtonMenu import ButtonMenu
from JsonManager import JsonManager

## UTILITY ##
from datetime import date
from datetime import datetime
import typing
import random
import time
import math

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
    
    ## LB COMMANDS ##
    
    @app_commands.command(description="Shows the top x people on the leaderboard.")
    @app_commands.describe(x = "Top x people")
    async def leaderboard(self,interaction=discord.Interaction,x:int=10):
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = users[user]["name"]
            money = users[user]["money"]
            leader_board[money] = name
            total.append(money)
        
        total = sorted(total,reverse=True)
        
        em = discord.Embed(title = "Top " + str(x) + " Richest People", description = "Based on the amount of money.",color=discord.Color(0xfa43ee))
        index = 1
        for amt in total:
            name = leader_board[amt]
            em.add_field(name = str(index) + ". " + name, value = str(amt), inline = False)
            if index == x:
                break
            else:
                index += 1
                
        await interaction.response.send_message(embed = em)
        
        
    @app_commands.command(description="Shows the top x people on the leaderboard for an item.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(x = "Top x people")
    async def topitem(self,interaction:discord.Interaction,item:str,x:int=10):
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = users[user]["name"]
            if "bag" in users[user].keys():
                for thing in users[user]["bag"]:
                    if thing['item'] == format(item):
                        total_amount = thing['amount']
                        if total_amount > 0:
                            leader_board[total_amount] = name
                            total.append(total_amount)
                        break
        
        total = sorted(total,reverse=True)
        
        em = discord.Embed(title = capital(item) + " Leaderboard", description = "Based on the amount of " + item +".",color=discord.Color(0xfa43ee))
        index = 1
        for amt in total:
            name = leader_board[amt]
            em.add_field(name = str(index) + ". " + name, value = str(amt), inline = False)
            if index == x:
                break
            else:
                index += 1
                
        await interaction.response.send_message(embed = em)
    
    
    
    
    
    ## USER INFO COMMANDS ##
    
    @app_commands.command(description="Shows how much energy you have, you can get more by eating food, and you use this to mine.")
    async def energy(self, interaction):
        user = interaction.user
        await open_account(user)
        users = await get_bank_data()
        
        
        await interaction.response.send_message(embed=discord.Embed(title = "**You have** " + str(users[str(user.id)]["energy"]) + " **energy!**",color=discord.Color.yellow()))
        
        
        
    @app_commands.command(description="Shows your balance.")
    async def balance(self, interaction):
        user = interaction.user
        await open_account(user)
        users = await get_bank_data()
        
        amt = users[str(user.id)]["money"]
        
        em = discord.Embed(title = user.name + "'s balance", color = discord.Color.yellow())
        em.add_field(name = "Balance", value = amt)
        await interaction.response.send_message(embed = em)
    
    
        
    @app_commands.command(description="Shows all the items in your bag.")
    async def bag(self, interaction):
        user = interaction.user
        await open_account(user)
        users = await get_bank_data()
        
        try:
            bag = users[str(user.id)]["bag"]
        except:
            bag = []
        
        c=0
        pages = []
        em = discord.Embed(title = "Bag 1/{}".format(math.ceil(len(bag)/21)))
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
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately your bag is empty.",color=discord.Color.red()))
    
    ## OFFERS/PAYING/LOAN ##
    
    @app_commands.command(description="Once a day you can collect payments from all your loans.")
    async def collectloan(self,interaction:discord.Interaction):
        users = await get_bank_data()
        user = interaction.user
        res = await getloans(users,user.id)
        if res == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**You can only do this once every day.**",color=discord.Color.red()))
            return
        users = res[0]
        if len(res[1]) < 1:
            await interaction.response.send_message(embed=discord.Embed(title = "**You have no outstanding loan payments.**",color=discord.Color.red()))
            return
        
        em = discord.Embed(title = "Collected Loan Payments",color=discord.Color.green())
        for pair in res[1]:
            users[pair[0]]["money"] -= pair[1]
            users[str(user.id)]["money"] += pair[1]
            em.add_field(name = users[pair[0]]["name"], value = pair[1])
        with open("mainbank.json",'w') as f:
            json.dump(users,f,indent=6,sort_keys=True)
        await interaction.response.send_message(embed=em)
    
    @app_commands.command(description="Once a loan request has been sent to you, this command will accept it.")
    async def acceptloan(self,interaction:discord.Interaction):
        global storedloan
        global noneloan
        user = interaction.user
        if storedloan == noneloan:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding loan request. If another loan request has taken place since a loan was requested from you, that loan request might have been erased.**",color=discord.Color.red()))
            return
        if user != storedloan[1]:
            await interaction.response.send_message(embed=discord.Embed(title="**You are not the intended recipient of this loan request. If another loan request has taken place since a loan was request from you, that loan request might have been erased.**",color=discord.Color.red()))
            return
        bal = await update_bank(user)
        if storedloan[2]>bal:
            await interaction.response.send_message(embed=discord.Embed(title="**Insufficient funds, loan cancelled.**",color=discord.Color.red()))
            return
        users = await get_bank_data()
        users = await addloan(users,storedloan[1].id,storedloan[0].id,storedloan[2])
        with open("mainbank.json",'w') as f:
            json.dump(users,f,indent=6,sort_keys=True)
        
        await update_bank(storedloan[1],-storedloan[2])
        await update_bank(storedloan[0],storedloan[2])
        
        await interaction.response.send_message(embed=discord.Embed(title="**You gave a loan of** " + str(storedloan[2]) + " **coins.**",color=discord.Color.green()))
        storedloan = noneloan

    @app_commands.command(description="Once a loan request has been sent to you, this command will deny it.")
    async def denyloan(self,interaction:discord.Interaction):
        global storedloan
        global noneloan
        user = interaction.user
        if storedloan == noneloan:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding loan request. If another loan request has taken place since a loan was requested from you, that loan request might have been erased.**",color=discord.Color.red()))
            return
        if user != storedloan[1]:
            await interaction.response.send_message(embed=discord.Embed(title="**You are not the intended recipient of this loan request. If another loan request has taken place since a loan was request from you, that loan request might have been erased.**",color=discord.Color.red()))
            return
        storedloan = noneloan
        await interaction.response.send_message(embed=discord.Embed(title="**You have denied this loan request.**",color=discord.Color.orange()))
        
    @app_commands.command(description="Cancels a loan request you have sent.")
    async def cancelloan(self,interaction:discord.Interaction):
        global storedloan
        global noneloan
        user = interaction.user
        if storedloan == noneloan:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding loan request. If another loan request has taken place since you requested a loan, your loan request might have been erased.**",color=discord.Color.red()))
            return
        if user != storedloan[0]:
            await interaction.response.send_message(embed=discord.Embed(title="**You did not send this loan request. If another loan request has taken place since you requested a loan, your loan request might have been erased.**",color=discord.Color.red()))
            return
        storedloan = noneloan
        await interaction.response.send_message(embed=discord.Embed(title="**You have cancelled this loan request.**",color=discord.Color.orange()))

    @app_commands.command(description="Requests <member> for a loan of <money> coins, they have to type \"/acceptloan\" to accept.")
    @app_commands.describe(member = "Member")
    @app_commands.describe(money = "Money in Loan")
    async def requestloan(self,interaction:discord.Interaction,member:discord.Member,money:int):
        global storedloan
        global noneloan
        user = interaction.user
        if member.bot:
            await interaction.response.send_message(embed=discord.Embed(title="**You cannot ask a bot for a loan.**",color=discord.Color.red()))
            return
        await open_account(user)
        await open_account(member)
        users = await get_bank_data()
        if await hasloan(users,user.id,member.id):
            await interaction.response.send_message(embed=discord.Embed(title=member.name + " **has already given you a loan, that must be paid off first before you can get another loan from them.**",color=discord.Color.red()))
            return
        bal = await update_bank(member)
        if bal < money:
            await interaction.response.send_message(embed=discord.Embed(title=member.name + " **does not have enough money to lend you a loan of** " + str(money) + "**.**",color=discord.Color.red()))
            return
        storedloan = [user,member,money]
        await interaction.response.send_message(embed=discord.Embed(title="**You requested** "+member.name+" **for a loan of ** " + str(money) + " **coins. You can use /cancelloan to cancel this, and they can use /acceptloan or /denyloan to accept or deny respectively.**",color=discord.Color.green()))
    
    @app_commands.command(description="Once an offer has been sent to you, this command will accept it.")
    async def acceptoffer(self,interaction:discord.Interaction):
        global storedoffer
        global noneoffer
        user = interaction.user
        if storedoffer == noneoffer:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outstanding offer. If another offer has taken place since an offer to you was proposed, that offer might have been erased, so ask them to send it again.**",color=discord.Color.red()))
            return
        if user != storedoffer[1]:
            await interaction.response.send_message(embed=discord.Embed(title="**You are not the intended recipient of this offer. If another offer has taken place since an offer to you was proposed, that offer might have been erased, so ask them to send it again.**",color=discord.Color.red()))
            return
        bal = await update_bank(user)
        if storedoffer[4]>bal:
            await interaction.response.send_message(embed=discord.Embed(title="**Insufficient funds, offer cancelled.**",color=discord.Color.red()))
            return
        users = await get_bank_data()
        users = await removefrombag(storedoffer[0],users,storedoffer[2],storedoffer[3])
        if users == None:
            await interaction.response.send_message(embed=discord.Embed(title="**They no longer have enough of this item in their bag.**",color=discord.Color.red()))
            return
        users = await addtobag(storedoffer[1],users,storedoffer[2],storedoffer[3])
        with open("mainbank.json",'w') as f:
            json.dump(users,f,indent=6,sort_keys=True)
        
        await update_bank(storedoffer[1],-storedoffer[4])
        await update_bank(storedoffer[0],storedoffer[4])
        
        await interaction.response.send_message(embed=discord.Embed(title="**You paid** " + str(storedoffer[4]) + " **coins for** " + str(storedoffer[3]) + " " + storedoffer[2] + "**.**",color=discord.Color.green()))
        storedoffer = noneoffer

    @app_commands.command(description="Once an offer has been sent to you, this command will deny it.")
    async def denyoffer(self,interaction:discord.Interaction):
        global storedoffer
        global noneoffer
        user = interaction.user
        if storedoffer == noneoffer:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding offer. If another offer has taken place since an offer to you was proposed, that offer might have been erased.**",color=discord.Color.red()))
            return
        if user != storedoffer[1]:
            await interaction.response.send_message(embed=discord.Embed(title="**You are not the intended recipient of this offer. If another offer has taken place since an offer to you was proposed, that offer might have been erased.**",color=discord.Color.red()))
            return
        storedoffer = noneoffer
        await interaction.response.send_message(embed=discord.Embed(title="**You have denied this offer.**",color=discord.Color.orange()))
        
    @app_commands.command(description="Cancels an offer you have sent.")
    async def canceloffer(self,interaction:discord.Interaction):
        global storedoffer
        global noneoffer
        user = interaction.user
        if storedoffer == noneoffer:
            await interaction.response.send_message(embed=discord.Embed(title="**There is no outsanding offer. If another offer has taken place since your offer, your offer might have been erased.**",color=discord.Color.red()))
            return
        if user != storedoffer[0]:
            await interaction.response.send_message(embed=discord.Embed(title="**You did not send this offer. If another offer has taken place since your offer, your offer might have been erased.**",color=discord.Color.red()))
            return
        storedoffer = noneoffer
        await interaction.response.send_message(embed=discord.Embed(title="**You have cancelled this offer.**",color=discord.Color.orange()))

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
            await interaction.response.send_message(embed=discord.Embed(title="**You cannot make an offer to a bot.**",color=discord.Color.red()))
            return
        if not (await valid_item(item)):
            await interaction.response.send_message(embed=discord.Embed(title="**Invalid item.**",color=discord.Color.red()))
            return
        await open_account(user)
        await open_account(member)
        users = await get_bank_data()
        if await removefrombag(user,users,item,amt) == None:
            await interaction.response.send_message(embed=discord.Embed(title="**You do not have enough of this item.**",color=discord.Color.red()))
            return
        storedoffer = [user,member,item,amt,price]
        await interaction.response.send_message(embed=discord.Embed(title="**You have made an offer to** "+member.name+" **of** " + str(amt) + " " + item + " **for** " + str(price) + " **coins. You can use /canceloffer to cancel this, and they can use /acceptoffer or /denyoffer to accept or deny respectively.**",color=discord.Color.green()))
        
    @app_commands.command(description="Pays money to a person.")
    @app_commands.describe(member = "Member")
    @app_commands.describe(amount = "Amount")
    async def pay(self,interaction:discord.Interaction,member:discord.Member,amount:int):
        if member.bot:
            await interaction.response.send_message(embed=discord.Embed(title="**You cannot pay a bot.**",color=discord.Color.red()))
            return
        user = interaction.user
        await open_account(user)
        await open_account(member)
        
        if amount == None:
            await interaction.response.send_message(embed=discord.Embed(title="**No amount entered, transaction cancelled.**",color=discord.Color.red()))
            return
        
        bal = await update_bank(user)
        
        amount = int(amount)
        if amount>bal:
            await interaction.response.send_message(embed=discord.Embed(title="**Insufficient funds, transaction cancelled.**",color=discord.Color.red()))
            return
        if amount<0:
            await interaction.response.send_message(embed=discord.Embed(title="**Amount must be positive, transaction cancelled.**",color=discord.Color.red()))
            return
        
        await update_bank(user,-amount)
        await update_bank(member,amount)
        
        await interaction.response.send_message(embed=discord.Embed(title="**You paid** " + str(amount) + " **coins to** "+member.name+"**!**",color=discord.Color.green()))
    
    
    
    
    ## BASIC MONEY/ITEM COMMANDS ##
    
    
    @app_commands.command(description="Consumes an item to get more energy.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(amount = "Amount")
    async def consume(self,interaction:discord.Interaction,item:str,amount:int = 1):
        user = interaction.user
        await open_account(user)
        
        res = await consume_this(user,item,amount)
        
        if res[0] > 0:
            if res[0] == 1:
                await interaction.response.send_message(embed=discord.Embed(title="**That Object isn't there!**",color=discord.Color.red()))
                return
            if res[0] == 2:
                await interaction.response.send_message(embed=discord.Embed(title=item + " **is not able to be consumed!**",color=discord.Color.red()))
                return
            if res[0] == 3:
                await interaction.response.send_message(embed=discord.Embed(title="**You don't have** " + str(amount) + " " + item + " **in your bag.**",color=discord.Color.red()))
                return
            if res[0] == 4:
                await interaction.response.send_message(embed=discord.Embed(title="**You don't have** " + item + " **in your bag.**",color=discord.Color.red()))
                return
            
        await interaction.response.send_message(embed=discord.Embed(title="**You just ate** " + str(amount) + " " + item + " **for** " + str(res[1]) + " **energy.**",color=discord.Color.green()))
        
    @app_commands.command(description="Bets money on a coinflip, if it lands on heads you win the amount, if it lands on tails you lose it.")
    @app_commands.describe(amount = "Amount")
    async def coinflip(self,interaction:discord.Interaction,amount:int):
        user = interaction.user
        await open_account(user)
        
        bal = await update_bank(user)
        
        amount = int(amount)
        if amount>bal:
            await interaction.response.send_message(embed=discord.Embed(title = "**Insufficient funds, coinflip cancelled.**",color=discord.Color.red()))
            return
        if amount<0:
            await interaction.response.send_message(embed=discord.Embed(title = "**Amount must be positive, coinflip cancelled.**",color=discord.Color.red()))
            return
        
        a = random.choice(["Heads","Tails"])
                           
        if a == "Heads":
            await interaction.response.send_message(embed=discord.Embed(title = "**The coin landed on heads\nYou won** " + str(amount),color=discord.Color.green()))
            await update_bank(user,amount)
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**The coin landed on tails\nYou paid** " + str(amount),color=discord.Color.orange()))
            await update_bank(user,-amount)
    
    @app_commands.command(description="Some random betting thing no idea how it works anymore.")
    @app_commands.describe(amount = "Amount")
    async def slots(self,interaction:discord.Interaction,amount:int):
        user = interaction.user
        await open_account(user)
        if amount == None:
            await interaction.response.send_message(embed=discord.Embed(title = "**No amount entered, slots cancelled.**",color=discord.Color.red()))
            return
        
        bal = await update_bank(user)
        
        amount = int(amount)
        if amount>bal:
            await interaction.response.send_message(embed=discord.Embed(title = "**Insufficient funds, slots cancelled.**",color=discord.Color.red()))
            return
        if amount<1:
            await interaction.response.send_message(embed=discord.Embed(title = "**Amount must be at least 1, slots cancelled.**",color=discord.Color.red()))
            return
        
        msg = "**You paid** " + str(amount) + "\n"
        await update_bank(user,-amount)
        
        final = []
        for i in range(3):
            a = random.choice(['X','O','Q','$'])
            
            final.append(a)
        
        msg += str(final) + "\n"
        
        if '$' == final[0] == final[1] == final[2]:
            await update_bank(user,20*amount)
            await interaction.response.send_message(embed=discord.Embed(title = msg + "**You won** " + str(20*amount) +"**!**",color=discord.Color.green()))
        elif final[0] == final[1] == final[2]:
            await update_bank(user,10*amount)
            await interaction.response.send_message(embed=discord.Embed(title = msg + "**You won** " + str(10*amount) +"**!**",color=discord.Color.green()))
        else:
            pity = 0
            if final[0] == '$':
                pity += 1
            if final[1] == '$':
                pity += 1
            if final[2] == '$':
                pity += 1
            if pity > 1:
                await update_bank(user,round(1.5*amount))
                await interaction.response.send_message(embed=discord.Embed(title = msg + "**You won** " + str(round(1.5*amount)) + "**!**",color=discord.Color.green()))
            elif pity > 0:
                await update_bank(user,10)
                await interaction.response.send_message(embed=discord.Embed(title = msg + "**You won** 10**!**",color=discord.Color.orange()))
            else:
                if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
                    await update_bank(user,round(0.1*amount))
                    await interaction.response.send_message(embed=discord.Embed(title = msg + "**You won** " + str(round(0.1*amount)) + "**!**",color=discord.Color.orange()))
                else:
                    await interaction.response.send_message(embed=discord.Embed(title = msg + "**You didn't win.**",color=discord.Color.orange()))
    
    @app_commands.command(description="Gets between 1 and 100 coins, can be used every day.")
    async def beg(self, interaction:discord.Interaction):
        user = interaction.user
        await open_account(user)
        earnings = await beg_this(user)
        if earnings == -1:
            await interaction.response.send_message(embed=discord.Embed(title = "**You can only do this once every day.**",color=discord.Color.red()))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "**Someone gave you** " + str(earnings) + " **coins!!**",color=discord.Color.green()))
        
    
    @app_commands.command(description="Buys a specified amount of an item from the shop.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(amount = "Amount")
    async def buy(self, interaction,item:str,amount:int=1):
        user = interaction.user
        await open_account(user)
        
        res = await buy_this(user,item,amount)
        
        if res[0]>0:
            if res[0]==1:
                await interaction.response.send_message(embed=discord.Embed(title = "**That Object isn't there!**",color=discord.Color.red()))
                return
            if res[0]==2:
                await interaction.response.send_message(embed=discord.Embed(title = str(amount) + " " + item + " **is unavailable.**",color=discord.Color.red()))
                return
            if res[0]==3:
                await interaction.response.send_message(embed=discord.Embed(title = "**You don't have enough money in your wallet to buy** " + str(amount) + " **of** " + item,color=discord.Color.red()))
                return
            if res[0]==4:
                await interaction.response.send_message(embed=discord.Embed(title = "**This item is not available on the market.**",color=discord.Color.red()))
                return
        
        
        await interaction.response.send_message(embed=discord.Embed(title = "**You just bought** " + str(amount) + " " + item + " **for** " + str(res[1]) + " **coins.**",color=discord.Color.green()))
    
    
    @app_commands.command(description="Sells a specified amount of an item back to the shop. 90% Refund Rate.")
    @app_commands.describe(item = "Item")
    @app_commands.describe(amount = "Amount")
    async def sell(self, interaction,item:str,amount:int = 1):
        user = interaction.user
        await open_account(user)
        
        res = await sell_this(user,item,amount)
        
        if res[0] > 0:
            if res[0] == 1:
                await interaction.response.send_message(embed=discord.Embed(title = "**That Object isn't there!**",color=discord.Color.red()))
                return
            if res[0] == 2:
                await interaction.response.send_message(embed=discord.Embed(title = "**You don't have** " + str(amount) + " " + item + " **in your bag.**",color=discord.Color.red()))
                return
            if res[0] == 3:
                await interaction.response.send_message(embed=discord.Embed(title = "**You don't have** " + item + " **in your bag.**",color=discord.Color.red()))
                return
            if res[0] == 4:
                await interaction.response.send_message(embed=discord.Embed(title = "**This item is not available on the market.**",color=discord.Color.red()))
                return
        
        await interaction.response.send_message(embed=discord.Embed(title = "**You just sold** " + str(amount) + " " + item + " **for** " + str(res[1]) + " **coins.**",color=discord.Color.green()))
        

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
            await open_account(user)
            users = await get_bank_data()
            bal = await update_bank(user)
            if bal < cost:
                await interaction.response.send_message(embed=discord.Embed(title = "**You cannot afford this, you need** " + str(cost) + "**.**",color=discord.Color.red()))
                return
            users = await addtobag(user,users,item[0],amount)
        
            with open("mainbank.json","w") as f:
                json.dump(users,f,indent=6,sort_keys=True)
            
            await update_bank(user,-cost)
            await interaction.response.send_message(embed=discord.Embed(title = "**You have bought** " + str(amount) + " " + item[0] + " **for** " + str(cost) + " **coins.**",color=discord.Color.green()))
            return
        if mode == "sell":
            cost = math.floor(cost*0.9)
            await open_account(user)
            users = await get_bank_data()
            bal = await update_bank(user)
            users = await removefrombag(user,users,item[0],amount)
            if users == None:
                await interaction.response.send_message(embed=discord.Embed(title = "**You do not have this many.**",color=discord.Color.red()))
                return
        
            with open("mainbank.json","w") as f:
                json.dump(users,f,indent=6,sort_keys=True)
            
            await update_bank(user,cost)
            await interaction.response.send_message(embed=discord.Embed(title = "**You have sold** " + str(amount) + " " + item[0] + " **for** " + str(cost) + " **coins.**",color=discord.Color.green()))
            return
        await interaction.response.send_message(embed=discord.Embed(title = "**The daily item is** " + item[0] + " **and it costs** " + str(cost) + "**.**",color=discord.Color.yellow()))
        return




    ### ITEMS ###

    @app_commands.command(name = "item", description = "Views the price and description of a particular item")
    @app_commands.describe(item = "Item")
    async def item(self, interaction: discord.Interaction, item: str):
        em = discord.Embed(title = f"{capital(item)} Info", color = discord.Color.blue())
        category = await get_item_category(item)
        price = await get_item_price(item)
        description = await get_item_description(item)
        energy = await get_item_energy(item)
        if category == 0:
            category = "Item not found!"
        if price == -1:
            price = "Out of Stock!"
        elif price == -2:
            price = "???"
        if description == 0:
            description = "Item not found!"
        em.add_field(name = "Price", value = price)
        if energy != 0: em.add_field(name = "Energy", value = energy)
        em.add_field(name = "Category", value = capital(category))
        em.add_field(name = "Description", value = description)
        await interaction.response.send_message(embed = em)
    
    
    
    
    
    @app_commands.command(name = "additem", description = "Just for ly ;)")
    @app_commands.choices(category = [
        Choice(name="Mining",value="mining"),
        Choice(name="Food",value="food"),
        Choice(name="Industrial",value="industrial"),
        Choice(name="Weapon",value="weapon"),
        Choice(name="Armor",value="armor"),
        Choice(name="Accessory",value="accessory"),
        Choice(name="Generic",value="generic")
    ])
    @app_commands.describe(item_name = "Item Name")
    @app_commands.describe(category = "Category")
    @app_commands.describe(description = "Description")
    @app_commands.describe(starting_price = "Starting Price")
    @app_commands.describe(starting_amount = "Starting Amount")
    @app_commands.describe(energy = "Energy")
    async def add_item(self, interaction: discord.Interaction, item_name: str, starting_price:int, starting_amount:int, category: typing.Optional[str] = "generic", description: typing.Optional[str] = "", energy:typing.Optional[int]=0):
        if interaction.user.id == 325691401851633674:
            await item_add(capital(item_name),description,format(category),starting_price,starting_amount,energy)
            await interaction.response.send_message("Added that item", ephemeral = True)
        else:
            await interaction.response.send_message("You are not ly ;)", ephemeral = True)





    @app_commands.command(name = "shop", description = "Shows all the items in the shop. Can specify a category, or use All.")
    @app_commands.choices(category = [
        Choice(name="All",value="all"),
        Choice(name="Mining",value="mining"),
        Choice(name="Food",value="food"),
        Choice(name="Industrial",value="industrial"),
        Choice(name="Weapon",value="weapon"),
        Choice(name="Armor",value="armor"),
        Choice(name="Accessory",value="accessory"),
        Choice(name="Generic",value="generic")
    ])
    @app_commands.describe(category = "Category")
    async def shop(self, interaction: discord.Interaction, category: typing.Optional[str] = "all"):
        pages = []
        items = await get_items()
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
                if await market_item_of(item):
                    newprice=await get_item_price_of(item)
                    if newprice>=price and not (name in item_names):
                        item_=item
                        price=newprice
                else:
                    target-=1
                    nonmarkets.append(item)
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['price']>0 and (category == "all" or category == item_['category']): sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
            for non in nonmarkets:
                items.remove(non)
        em = discord.Embed(title = "Market{} 1/{}".format("" if category == "all" else " {}".format(capital(category)), math.ceil(len(sorted_items)/18)))
        for item in sorted_items:
            name = item['name']
            price = await get_item_price(format(name))
            start = str(price)
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
                em = discord.Embed(title = "Market{} {}/{}".format("" if category == "all" else " {}".format(capital(category)), len(pages)+1, math.ceil(len(sorted_items)/18)))
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=discord.Color.red()))

    @app_commands.command(name = "itemlist", description = "Shows all the items. Can specify a category, or use All.")
    @app_commands.choices(category = [
        Choice(name="All",value="all"),
        Choice(name="Mining",value="mining"),
        Choice(name="Food",value="food"),
        Choice(name="Industrial",value="industrial"),
        Choice(name="Weapon",value="weapon"),
        Choice(name="Armor",value="armor"),
        Choice(name="Accessory",value="accessory"),
        Choice(name="Generic",value="generic")
    ])
    @app_commands.describe(category = "Category")
    async def itemlist(self, interaction: discord.Interaction, category: typing.Optional[str] = "all"):
        pages = []
        items = await get_items()
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
                if category == "all" or category == item_['category']: sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
        em = discord.Embed(title = "Item List{} 1/{}".format("" if category == "all" else " {}".format(capital(category)), math.ceil(len(sorted_items)/18)))
        for item in sorted_items:
            name = item['name']
            price = await get_item_price(format(name))
            desc = item["description"]
            em.add_field(name = name, value = desc)
            count += 1
            if count > 17:
                count = 0
                pages.append(em)
                em = discord.Embed(title = "Item List{} {}/{}".format("" if category == "all" else " {}".format(capital(category)), len(pages)+1, math.ceil(len(sorted_items)/18)))
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=discord.Color.red()))










    @app_commands.command(name = "shortshop", description = "Shows all the items in the shop. Can specify a category, or use All.")
    @app_commands.choices(category = [
        Choice(name="All",value="all"),
        Choice(name="Mining",value="mining"),
        Choice(name="Food",value="food"),
        Choice(name="Industrial",value="industrial"),
        Choice(name="Weapon",value="weapon"),
        Choice(name="Armor",value="armor"),
        Choice(name="Accessory",value="accessory"),
        Choice(name="Generic",value="generic")
    ])
    @app_commands.describe(category = "Category")
    async def shortshop(self, interaction: discord.Interaction, category: typing.Optional[str] = "all"):
        pages = []
        items = await get_items()
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
                if await market_item_of(item):
                    newprice=await get_item_price_of(item)
                    if newprice>=price and not (name in item_names):
                        item_=item
                        price=newprice
                else:
                    target-=1
                    nonmarkets.append(item)
            if not (item_ is None):
                item_names.append(item_['name'])
                if item_['price']>0 and (category == "all" or category == item_['category']): sorted_items.append(item_)
                lensorteditems += 1
                items.remove(item_)
            for non in nonmarkets:
                items.remove(non)
        em = discord.Embed(title = "Market{} 1/{}".format("" if category == "all" else " {}".format(capital(category)), math.ceil(len(sorted_items)/18)))
        for item in sorted_items:
            name = item['name']
            price = await get_item_price(format(name))
            start = str(price)
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
                em = discord.Embed(title = "Market{} {}/{}".format("" if category == "all" else " {}".format(capital(category)), len(pages)+1, math.ceil(len(sorted_items)/18)))
        if count > 0:
            pages.append(em)
        if len(pages)>0:
            await interaction.response.send_message(embeds=pages[0] if isinstance(pages[0],list) else [pages[0]], view=ButtonMenu(pages,300,interaction.user))
        else:
            await interaction.response.send_message(embed=discord.Embed(title = "Unfortunately no items could be found in that category.",color=discord.Color.red()))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### USERS ###
    
async def beg_this(user):
    users = await get_bank_data()
    try:
        if str(date.today()) == users[str(user.id)]["lastbeg"]:
            return -1
    except:
        pass
    earnings = random.randrange(101)
    users[str(user.id)]["money"] += earnings
    users[str(user.id)]["lastbeg"] = str(date.today())
    with open("mainbank.json",'w') as f:
        json.dump(users,f,indent=6,sort_keys=True)
    return earnings

async def open_account(user):
    users = await get_bank_data()
        
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]= {}
        users[str(user.id)]["name"] = user.name
        users[str(user.id)]["money"] = 200
        users[str(user.id)]["energy"] = 100
        users[str(user.id)]["pumpkinseed"] = False
        users[str(user.id)]["processes"] = []
        users[str(user.id)]["factories"] = {}
        users[str(user.id)]["equipment"] = ["None","None","None"]
        
    with open("mainbank.json",'w') as f:
        json.dump(users,f,indent=6,sort_keys=True)
    return True

    
async def get_bank_data():
    with open("mainbank.json",'r') as f:
        users = json.load(f)
    return users

async def update_bank(user,change = 0):
    users = await get_bank_data()
    
    users[str(user.id)]["name"] = user.name
    users[str(user.id)]["money"] += change
    
    with open("mainbank.json",'w') as f:
        json.dump(users,f,indent=6,sort_keys=True)
        
    bal = users[str(user.id)]["money"]
    return bal

async def update_bank_by_id(id,change = 0):
    users = await get_bank_data()
    
    users[str(id)]["money"] += change
    
    with open("mainbank.json",'w') as f:
        json.dump(users,f,indent=6,sort_keys=True)
        
    bal = users[str(id)]["money"]
    return bal

async def update_energy(user,change = 0):
    users = await get_bank_data()
    
    users[str(user.id)]["name"] = user.name
    users[str(user.id)]["energy"] += change
    
    with open("mainbank.json",'w') as f:
        json.dump(users,f,indent=6,sort_keys=True)
        
    energy = users[str(user.id)]["energy"]
    return energy











### ITEMS ###

## MARKET STUFF ##

def get_daily_item():
    dailyitems = [("screw",5),("cake",6),("rubber",30),("cake",5),("rawsilicon",15),("cake",4),("screw",6),("cake",7),("rubber",25),("cake",3),("rawsilicon",20),("cake",5)]
    return dailyitems[datetime.now().day % len(dailyitems)]

async def getloans(users,loanerid):
    try:
        if str(date.today()) == users[str(loanerid)]["lastinterest"]:
            return -1
    except:
        pass
    try:
        pairs = []
        ids = []
        for id,value in users[str(loanerid)]["loans"].items():
            if value[0] > 0:
                ids.append(id)
        for id in ids:
            users[str(loanerid)]["loans"][id][0] -= 1
            pairs.append((id,round(users[str(loanerid)]["loans"][id][1]/10)))
        users[str(loanerid)]["lastinterest"] = str(date.today())
        return (users,pairs)
    except:
        return (users,[])

async def addloan(users,loanerid,loaneeid,amount):
    try:
        users[str(loanerid)]["loans"][str(loaneeid)] = [11,amount]
    except:
        users[str(loanerid)]["loans"] = {str(loaneeid):[11,amount]}
    return users

async def hasloan(users,loanerid,loaneeid):
    try:
        return users[str(loanerid)]["loans"][str(loaneeid)][0] > 0
    except:
        return False

async def addtobag(author,users,item,amount):
    item = format(item)
    try:
        index = 0
        t = False
        for thing in users[str(author.id)]["bag"]:
            n = thing["item"]
            if n == item:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(author.id)]["bag"][index]["amount"] = new_amt
                t = True
                break
            index+=1
        if t == False:
            obj = {"item": item, "amount" : amount}
            users[str(author.id)]["bag"].append(obj)
    except:
        obj = {"item": item,"amount": amount}
        users[str(author.id)]["bag"] = [obj]
    return users

async def removefrombag(user,users,item,amount):
    item = format(item)
    try:
        index = 0
        t = False
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if format(n) == format(item):
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return None
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                return users
            index+=1
        return None
    except Exception as e:
        print(e)
        return None


    
async def consume_this(user,item_name,amount,price=None):
    item_name = item_name.lower()
    valid = await valid_item(item_name)
    if valid:
        energyper = await get_item_energy(item_name)
    else:
         return [1,0]
        
    if energyper < 1:
        return [2,0]
    energy = energyper*amount
    if item_name == "milk" or item_name == "cookie":
        energy=0
    users = await get_bank_data()
    
    try:
        index = 0
        t = False
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if format(n) == format(item_name):
                old_amt = thing["amount"]
                if old_amt < amount:
                    return [3,0]
                new_amt = old_amt - amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                with open("mainbank.json",'w') as f:
                    json.dump(users,f,indent=6,sort_keys=True)
                t = True
                break
            index+=1
        if t == False:
            return [4,0]
    except:
        return [4,0]
        
    await update_energy(user,energy)
    
    return [0,energy]

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    valid = await valid_item(item_name)
    if valid:
        valid = await market_item(item_name)
    else:
        return [4,0]
    if valid:
        price = await get_item_price(item_name,bamount=amount)
    else:
        return [1,0]
    
    #available = await available_item(item_name,amount)
    #if not available:
    #    await update_item(item_name,amount)
    #    return [2,0]
    
    if price > 0 and price < 1:
        price = 1 
    cost = price*amount
    users = await get_bank_data()
    
    bal = await update_bank(user)
                           
    if bal<cost:
        return [3,0]
                           
    try:
        index = 0
        t = False
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = True
                break
            index+=1
        if t == False:
            obj = {"item":item_name, "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name,"amount":amount}
        users[str(user.id)]["bag"] = [obj]
    
    
    await update_item(item_name,-amount)
    
    with open("mainbank.json","w") as f:
        json.dump(users,f,indent=6,sort_keys=True)
        
    await update_bank(user,-cost)
                      
    return [0,cost]

async def sell_this(user,item_name,amount):
    item_name = item_name.lower()
    valid = await valid_item(item_name)
    if valid:
        valid = await market_item(item_name)
    else:
        return [4,0]
    if valid:
        baseprice = await get_item_price(item_name,samount=amount)
        price = baseprice
    else:
         return [1,0]
        
    if price > 0 and price < 1:
        price = 1
    cost = (int) (price*amount*0.9)
    users = await get_bank_data()
    
    try:
        index = 0
        t = False
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if format(n) == format(item_name):
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [2,0]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                with open("mainbank.json",'w') as f:
                    json.dump(users,f,indent=6,sort_keys=True)
                t = True
                break
            index+=1
        if t == False:
            return [3,0]
    except:
        return [3,0]
        
    await update_item(item_name,amount)
    
    await update_bank(user,cost)
    
    return [0,cost]

## ITEM INFO ##

async def get_items():
    with open("items.json",'r') as f:
        items = json.load(f)
    return items

async def valid_item(item_name):
    items = await get_items()
    for item in items:
        if format(item['name']) == format(item_name):
            return True
    return False

async def market_item(item_name):
    items = await get_items()
    for item in items:
        if format(item['name']) == format(item_name):
            return item['price'] > 0
    return False

async def market_item_of(item):
    return item['price'] > 0
    
async def get_item_price(item_name,bamount=1,samount=1):
    if bamount<1:bamount=1
    if samount<1:samount=1
    items = await get_items()
    for item in items:
        if format(item['name']) == format(item_name):
            if not await market_item_of(item):
                return -2
            price = round(item['price']*(item['bought']+bamount-1)/(item['sold']+samount-1))
            if price < 1:
                price = 1
            return (int) (price)
    return -2
    
async def get_item_price_of(item,bamount=1,samount=1):
    if bamount<1:bamount=1
    if samount<1:samount=1
    if not await market_item_of(item):
        return -2
    price = round(item['price']*(item['bought']+bamount-1)/(item['sold']+samount-1))
    if price < 1:
        price = 1
    return (int) (price)
    
async def get_item_energy(item_name):
    items = await get_items()
    for item in items:
        if format(item['name']) == format(item_name):
            return item['energy']
    return 0
    
async def get_item_category(item_name):
    items = await get_items()
    for item in items:
        if format(item['name']) == format(item_name):
            return item['category']
    return 0
    
async def get_item_description(item_name):
    items = await get_items()
    for item in items:
        if format(item['name']) == format(item_name):
            return item['description']
    return 0

async def item_add(item_name:str,description:str,category:str,starting_price:int,starting_amount:int,energy:int):
    items = await get_items()
    
    items.append({"name":item_name,"category":category,"description":description,"price":starting_price,"bought":starting_amount,"sold":starting_amount,"energy":energy})
    
    with open("items.json",'w') as f:
        json.dump(items,f,indent=6,sort_keys=True)
    
    
    with open("itemsog.json",'r') as f:
        items = json.load(f)
    
    items.append({"name":item_name,"category":category,"description":description,"price":starting_price,"bought":starting_amount,"sold":starting_amount,"energy":energy})
    
    with open("itemsog.json",'w') as f:
        json.dump(items,f,indent=6,sort_keys=True)

async def update_item(item_name,change = 0):
    items = await get_items()
    
    index = 0
    for item in items:
        if format(item['name']) == format(item_name):
            if change > 0: items[index]['sold'] += change
            else: items[index]['bought'] -= change
        index+=1
    
    with open("items.json",'w') as f:
        json.dump(items,f,indent=6,sort_keys=True)








### STRING ###

def format(str):
    newstr = ""
    for c in str:
        if not c == ' ':
            newstr += c
    return newstr.lower()

def capital(str):
    if " " in str:
        return " ".join(capital(s) for s in str.split(" "))
    newstr = ""
    first = True
    for c in str:
        if first:
            newstr += c.upper()
            first = False
        else:
            newstr += c.lower()
    return newstr



### MISC ###


def curTime():
    return round(time.time() * 1000)






### FINAL ###

async def setup(bot:commands.Bot):
    await bot.add_cog(ItemCommands(bot),guilds=[discord.Object(id=490588110590181376)])