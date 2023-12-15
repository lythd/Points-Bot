
#---------------------------------------------------------------------------SETUP----------------------------------------------------------------------------------------#

### IMPORTS ###

## MY OWN ##
from ButtonMenu import ButtonMenu
from JsonManager import *
from GeneralFunctions import *
from UserFunctions import *

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













#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### GENERAL ###

## MARKET STUFF ##

def get_daily_item():
    dailyitems = [("screw",5),("cake",6),("rubber",30),("cake",5),("rawsilicon",15),("cake",4),("screw",6),("cake",7),("rubber",25),("cake",3),("rawsilicon",20),("cake",5)]
    return dailyitems[datetime.now().day % len(dailyitems)]

def getloans(loanerid):
    users = getUsers()
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
        return pairs
    except:
        return []

def addloan(loanerid,loaneeid,amount):
    users = getUsers()
    try:
        users[str(loanerid)]["loans"][str(loaneeid)] = [11,amount]
    except:
        users[str(loanerid)]["loans"] = {str(loaneeid):[11,amount]}

def hasloan(loanerid,loaneeid):
    users = getUsers()
    try:
        return users[str(loanerid)]["loans"][str(loaneeid)][0] > 0
    except:
        return False

def addtobag(author,item,amount=1):
    users = getUsers()
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

def addalltobag(author,items):
    for item,amount in items.items():
        addtobag(author,item,amount)

def amountinbag(author,item):
    users = getUsers()
    item = format(item)
    try:
        index = 0
        t = False
        for thing in users[str(author.id)]["bag"]:
            n = thing["item"]
            if n == item: return thing["amount"]
            index+=1
        if t == False: return 0
    except:
        return 0

def removefrombag(user,item,amount=1):
    users = getUsers()
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
                    return -1
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                return 1
            index+=1
    except Exception as e:
        print(e)
    return -1

def removeallfrombag(author,items):
    for item,amount in items.items():
        if amountinbag(author,item) < amount: return -1
    for item,amount in items.items():
        removefrombag(author,item,amount)










## STATS ##

def addmobkills(author,mob,amount=1):
    users = getUsers()
    mob = format(mob)
    try:
        index = 0
        t = False
        for thing in users[str(author.id)]["mobkills"]:
            n = thing["mob"]
            if n == mob:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(author.id)]["mobkills"][index]["amount"] = new_amt
                t = True
                break
            index+=1
        if t == False:
            obj = {"mob": mob, "amount" : amount}
            users[str(author.id)]["mobkills"].append(obj)
    except:
        obj = {"mob": mob,"amount": amount}
        users[str(author.id)]["mobkills"] = [obj]

def getmobkills(author,mob):
    users = getUsers()
    mob = format(mob)
    try:
        index = 0
        t = False
        for thing in users[str(author.id)]["mobkills"]:
            n = thing["mob"]
            if n == mob: return thing["amount"]
            index+=1
        if t == False: return 0
    except:
        return 0

def addmobkos(author,mob,amount=1):
    users = getUsers()
    mob = format(mob)
    try:
        index = 0
        t = False
        for thing in users[str(author.id)]["mobkos"]:
            n = thing["mob"]
            if n == mob:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(author.id)]["mobkos"][index]["amount"] = new_amt
                t = True
                break
            index+=1
        if t == False:
            obj = {"mob": mob, "amount" : amount}
            users[str(author.id)]["mobkos"].append(obj)
    except:
        obj = {"mob": mob,"amount": amount}
        users[str(author.id)]["mobkos"] = [obj]

def getmobkos(author,mob):
    users = getUsers()
    mob = format(mob)
    try:
        index = 0
        t = False
        for thing in users[str(author.id)]["mobkos"]:
            n = thing["mob"]
            if n == mob: return thing["amount"]
            index+=1
        if t == False: return 0
    except:
        return 0

def addwins(author,amount=1):
    users = getUsers()
    try:
        users[str(author.id)]["wins"] += amount
    except:
        users[str(author.id)]["wins"] = amount

def getwins(author):
    users = getUsers()
    try:
        return users[str(author.id)]["wins"]
    except:
        return 0

def addlosses(author,amount=1):
    users = getUsers()
    try:
        users[str(author.id)]["losses"] += amount
    except:
        users[str(author.id)]["losses"] = amount

def getlosses(author):
    users = getUsers()
    try:
        return users[str(author.id)]["losses"]
    except:
        return 0

def addvictories(author,person,amount=1):
    users = getUsers()
    person = format(person)
    try:
        index = 0
        t = False
        for thing in users[str(author.id)]["victories"]:
            n = thing["person"]
            if n == person:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(author.id)]["victories"][index]["amount"] = new_amt
                t = True
                break
            index+=1
        if t == False:
            obj = {"person": person, "amount" : amount}
            users[str(author.id)]["victories"].append(obj)
    except:
        obj = {"person": person,"amount": amount}
        users[str(author.id)]["victories"] = [obj]

def getvictories(author,person):
    users = getUsers()
    person = format(person)
    try:
        index = 0
        t = False
        for thing in users[str(author.id)]["victories"]:
            n = thing["person"]
            if n == person: return thing["amount"]
            index+=1
        if t == False: return 0
    except:
        return 0










## THIS ##
    
def consume_this(user,item_name,amount,price=None):
    item_name = format(item_name)
    valid = valid_item(item_name)
    if valid:
        energyper = get_food_energy(item_name)
    else:
         return [1,0]
        
    if energyper == 0:
        return [2,0]
    energy = energyper*amount
    
    users = getUsers()
    
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
                writeUsers()
                t = True
                break
            index+=1
        if t == False:
            return [4,0]
    except:
        return [4,0]
        
    update_energy(user,energy)
    
    return [0,energy]

def buy_this(user,item_name,amount):
    item_name = format(item_name)
    valid = valid_item(item_name)
    if valid:
        valid = market_item(item_name)
    else:
        return [4,0]
    if valid:
        price = get_item_price(item_name,bamount=amount)
    else:
        return [1,0]
    
    if price > 0 and price < 1:
        price = 1 
    cost = price*amount
    users = getUsers()
    
    bal = update_bank(user)
                           
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
    
    
    update_item(item_name,-amount)
    
    writeUsers()
        
    update_bank(user,-cost)
                      
    return [0,cost]

def sell_this(user,item_name,amount):
    item_name = format(item_name)
    valid = valid_item(item_name)
    if valid:
        valid = market_item(item_name)
    else:
        return [4,0]
    if valid:
        baseprice = get_item_price(item_name,samount=amount)
        price = baseprice
    else:
         return [1,0]
        
    if price > 0 and price < 1:
        price = 1
    cost = (int) (price*amount*0.9)
    users = getUsers()
    
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
                writeUsers()
                t = True
                break
            index+=1
        if t == False:
            return [3,0]
    except:
        return [3,0]
        
    update_item(item_name,amount)
    
    update_bank(user,cost)
    
    return [0,cost]




























### ITEM INFO ###

def value_of_items(items):
    val = 0
    for item in items:
        price = get_item_price(item['item'])
        if price != -1:
            val += price * item['amount']
    return val

def valid_item(item_name):
    items = getItems()
    for item in items:
        if format(item['name']) == format(item_name):
            return True
    return False

def market_item(item_name):
    items = getItems()
    for item in items:
        if format(item['name']) == format(item_name):
            return item['price'] > 0
    return False

def market_item_of(item):
    return item['price'] > 0
    
def get_item_price(item_name,bamount=1,samount=1):
    if bamount<1:bamount=1
    if samount<1:samount=1
    items = getItems()
    for item in items:
        if format(item['name']) == format(item_name):
            if not market_item_of(item):
                return -1
            price = round(item['price']*(item['bought']+bamount-1)/(item['sold']+samount-1))
            if price < 1:
                price = 1
            return (int) (price)
    return -1
    
def get_item_price_of(item,bamount=1,samount=1):
    if bamount<1:bamount=1
    if samount<1:samount=1
    if not market_item_of(item):
        return -1
    price = round(item['price']*(item['bought']+bamount-1)/(item['sold']+samount-1))
    if price < 1:
        price = 1
    return (int) (price)
    
def get_item_category(item_name):
    items = getItems()
    for item in items:
        if format(item['name']) == format(item_name):
            return item['category']
    return -1
    
def get_item_desc(item_name):
    items = getItems()
    for item in items:
        if format(item['name']) == format(item_name):
            return item['description']
    return -1
    
def get_food_energy(item_name):
    foods = getFoods()
    try:
        return foods[format(item_name)]['energy']
    except:
        return -1
    
def get_pickaxe_tier(item_name):
    pickaxes = getPickaxes()
    for pickaxe,data in pickaxes.items():
        if pickaxe == format(item_name):
            return data['tier']
    return -1
    
def get_pickaxe_doc(item_name):
    pickaxes = getPickaxes()
    for pickaxe,data in pickaxes.items():
        if pickaxe == format(item_name):
            return data['double']
    return -1
    
def get_pickaxe_dur(item_name):
    pickaxes = getPickaxes()
    for pickaxe,data in pickaxes.items():
        if pickaxe == format(item_name):
            return data['durability']
    return -1
    
def get_rod_fp(item_name):
    rods = getRods()
    for rod,data in rods.items():
        if rod == format(item_name):
            return data['fp']
    return -1
    
def get_rod_lbc(item_name):
    rods = getRods()
    for rod,data in rods.items():
        if rod == format(item_name):
            return data['lbc']
    return -1
    
def get_rod_bcc(item_name):
    rods = getRods()
    for rod,data in rods.items():
        if rod == format(item_name):
            return data['bcc']
    return -1
    
def get_rod_dur(item_name):
    rods = getRods()
    for rod,data in rods.items():
        if rod == format(item_name):
            return data['durability']
    return -1
    
def get_weapon_pdmg(item_name):
    weapons = getWeapons()
    for weapon,data in weapons.items():
        if weapon == format(item_name):
            return data['piercing']
    return -1
    
def get_weapon_bdmg(item_name):
    weapons = getWeapons()
    for weapon,data in weapons.items():
        if weapon == format(item_name):
            return data['blunt']
    return -1
    
def get_weapon_dur(item_name):
    weapons = getWeapons()
    for weapon,data in weapons.items():
        if weapon == format(item_name):
            return data['durability']
    return -1
    
def get_weapon_effects(item_name):
    weapons = getWeapons()
    for weapon,data in weapons.items():
        if weapon == format(item_name):
            return data['effects']
    return []
    
def get_armor_def(item_name):
    armors = getArmor()
    for armor,data in armors.items():
        if armor == format(item_name):
            return data['defense']
    return -1
    
def get_armor_dur(item_name):
    armors = getArmor()
    for armor,data in armors.items():
        if armor == format(item_name):
            return data['durability']
    return -1
    
def get_armor_effects(item_name):
    armors = getArmor()
    for armor,data in armors.items():
        if armor == format(item_name):
            return data['effects']
    return []
    
def get_accessory_dur(item_name):
    accessories = getAccessories()
    for accessory,data in accessories.items():
        if accessory == format(item_name):
            return data['durability']
    return -1
    
def get_accessory_effects(item_name):
    accessories = getAccessories()
    for accessory,data in accessories.items():
        if accessory == format(item_name):
            return data['effects']
    return []
    
def get_ammo_pdmg(item_name):
    ammos = getAmmo()
    for ammo,data in ammos.items():
        if ammo == format(item_name):
            return data['piercing']
    return -1
    
def get_ammo_bdmg(item_name):
    ammos = getAmmo()
    for ammo,data in ammos.items():
        if ammo == format(item_name):
            return data['blunt']
    return -1
    
def get_ammo_effects(item_name):
    ammos = getAmmo()
    for ammo,data in ammos.items():
        if ammo == format(item_name):
            return data['effects']
    return []
    
def get_bait_fp(item_name):
    baits = getBait()
    for bait,data in baits.items():
        if bait == format(item_name):
            return data['fp']
    return -1
    
def get_bait_drop(item_name):
    baits = getBait()
    for bait,data in baits.items():
        if bait == format(item_name):
            return data['drop']
    return 'None'
    
def get_bait_effects(item_name):
    baits = getBait()
    for bait,data in baits.items():
        if bait == format(item_name):
            return data['effects']
    return []










### MORE GENERAL STUFF ###

def percentage_chance(chance): #for crit chance, bcc, acc, doc, etc
    if chance < 1: return False
    if chance > 99: return True
    return random.randrange(0,100) < chance

def reciprocal_chance(chance): #for durability, etc
    if chance < 1: return False
    if chance == 1: return True
    return random.randrange(0,chance) < 1

def parse_number(number): #for drop amount, etc
    if isinstance(number,list): return random.randrange(number[0],number[1]+1)
    return number

def break_message(durability):
    if durability < 2:
        return "has been used"
    return "has broken"

def get_categories():
    return [("Generic","generic"),("Mining","mining"),("Food","food"),("Industrial","industrial"),("Pickaxes","pickaxe"),("Fishing Rods","rod"),("Weapons","weapon"),("Armor","armor"),("Accessories","accessory"),("Ammo","arrow,rocket,cometfragment"),("Bait","bait")]

def get_effect_description(effect):
    effects = ["goesfirst","goeslast","magic","evenout","speedboost","defensebasher","fragile","surprise","criticalchance","elasticpotential","lightweight","doublehit","multihit","alwaysgoesfirst","soothing","bow","rocketlauncher","starlauncher","alwaysgoeslast","reallyalwaysgoeslast","powerup","thornsdamage","regenerator","blessed","countermagic","mana","ranger","slash","morehealth","pricklyshield","weaklybuffed","buffed","stronglybuffed","rawpower","hookedon","lightspeed","shielded","breakable","sacrificial","strength","turtled","cactusificated","ironified","evil","tough","magicguard","golden","hard","block","sharp","dense","healup","beetled","wall","fishingbuff","strongfishingbuff","fishingboost","miningbuff","strongminingbuff","miningboost","lavafishing","silky","deepdark","withering","explosion","wings","scary","lucky"]
    descs = ["+1 move priority.","-1 move priority.","Requires mana crystal, ignores enemy defense, and consumes mana crystal.","Reduces defense by half and increases attack by reduced amount.","Increases damage by half your speed.","Increases damage by half of enemy defense.","Breaks when attacking something with at least 300 defense.","Triples your damage if you move first.","+20% chance to ignore defense, default is 0.","Recoils with double the damage received.","+20 speed.","Hits twice in a row.","Hits randomly between 1-5 times in a row.","+2 move priority.","Opponent deals half damage.","Uses arrows.","Uses rockets.","Uses comet fragments.","-2 move priority.","-100 move priority.","Doubles damage after each turn.","+30 damage.","Regens half of max health after taking damage.","+100 max health, and regens 50 health after taking damage.","Does half damage if enemy has a mana crystal.","Allows use of magic weapons.","+40 damage on ammo.","x1.2 piercing damage.","+100 max health.","+80 damage, +125 defense.","+30 in each stat.","+60 in each stat.","+90 in each stat.","If your total damage is less than 200 then it will become 200, otherwise +50 damage.","+170 speed, +30 damage.","+500 speed.","Prevents enemy attacks of less than 500 damage from going first.","Enemy attacks of at least 300 damage will break this item.","Instead of an item breaking this will use instead.","x1.5 damage.","x3 defense, x0.5 damage, x0.5 speed.","x2 piercing damage.","x1.5 blunt damage, x1.25 defense.","+50 max health, +100 defense.","Half of incoming magic damage is reduced.","-50 max health, +50 defense, +100 damage.","x1.25 piercing damage, x1.75 blunt damage.","+100 defense.","Always blocks the first hit completely.","Ignores up to 50 enemy defense.","Ignores up to 50 enemy blunt damage.","Fully regenerates health after every attack, but reduces damage by x0.75.","x2 defense, x0.5 speed.","+200 defense.","+25 fishing power.","+50 fishing power.","x1.25 fishing power and -25% bait consumption chance.","+10% double ore chance.","+25% double ore chance.","x1.25 double ore chance.","Allows fishing in lava.","Fishing line never breaks.","Prevents enemy from seeing, halving their movement speed.","Deals 100 damage ignoring defense to enemy.","A one-time explosion, goes through half of defense.","Allows you to fly into the clouds.","Scares common and uncommon fish away.","+20% double ore chance, -25% bait consumption chance, -5% line break chance, +2% special drop chance."]
    return descs[effects.index(format(effect))]







### ITEM DO ###

def item_add(item_name:str,description:str,category:str,starting_price:int,starting_amount:int,energy:int):
    items = getItems()
    items.append({"name":item_name,"category":category,"description":description,"price":starting_price,"bought":starting_amount,"sold":starting_amount,"energy":energy})
    writeItems()
    
    items = getItemsOg()
    items.append({"name":item_name,"category":category,"description":description,"price":starting_price,"bought":starting_amount,"sold":starting_amount,"energy":energy})
    writeItemsOg()

def update_item(item_name,change = 0):
    items = getItems()
    
    index = 0
    for item in items:
        if format(item['name']) == format(item_name):
            if change > 0: items[index]['sold'] += change
            else: items[index]['bought'] -= change
        index+=1
    
    writeItems()
















