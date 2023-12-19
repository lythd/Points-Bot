
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













#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### EQUIPMENT ###

def generate_equipment(name,stats):
    em = discord.Embed(title = name + "'s Equipment", color = colorEquipment())
    desc0 = "Weapons are overrated anyway."
    desc1 = ""
    desc2 = ""
    desc3 = ""

    items = getItems()
    if stats['0'] != "fist":
        for item in items:
            if format(item['name']) == format(stats['0']):
                desc0 = item['description']
                break
    if stats['1'] != "none":
        for item in items:
            if format(item['name']) == format(stats['1']):
                desc1 = item['description']
                break
    if stats['2'] != "none":
        for item in items:
            if format(item['name']) == format(stats['2']):
                desc2 = item['description']
                break
    if stats['3'] != "none":
        for item in items:
            if format(item['name']) == format(stats['3']):
                desc3 = item['description']
                break
    em.add_field(name = "Main: " + capital(stats['0']), value = desc0)
    em.add_field(name = "Armor: " + capital(stats['1']), value = desc1)
    em.add_field(name = "Accessory: " + capital(stats['2']), value = desc2)
    if stats['3'] != "none": em.add_field(name = "Ammo: " + capital(stats['3']), value = desc3)
    return em

def generate_stats(name,stats):
    em = discord.Embed(title = name + "'s Stats", color = colorEquipment())

    #apply multipliers
    for s in ['pdmg','bdmg','doc','fp']:
        if stats[s] != -1: stats[s] *= stats[s+'-m']
    #toc
    stats['toc'] = -1
    if stats['doc'] > 100:
        stats['toc'] = stats['doc'] - 100
        stats['doc'] = 100
    #-1 stats
    attr = [("Piercing Damage","pdmg"),("Blunt Damage","bdmg"),("Mining Tier","tier"),("Double Ore Chance","doc"),("Triple Ore Chance","toc"),("Fishing Power","fp"),("Line Break Chance","lbc"),("Bait Consumption Chance","bcc"),("Special Drop Chance","sdc"),("Ammo Consumption Chance","acc"),("Main Durability","dur0"),("Armor Durability","dur1"),("Accessory Durability","dur2")]
    for n,i in attr:
        if stats[i] != -1: em.add_field(name = n, value = round(stats[i]))
    #0 stats
    attr = [("Max Health","mhp"),("Defense","def"),("Speed","spd"),("Regeneration","reg")]
    for n,i in attr:
        if stats[i] != 0: em.add_field(name = n, value = round(stats[i]))
    #string stats
    attr = [("Special Drop","drop")]
    for n,i in attr:
        if stats[i] != 'None': em.add_field(name = n, value = round(stats[i]))
    #move priority    
    if stats['mp'] != 0: em.add_field(name = 'Move Priority', value = "{}{}".format("+" if stats['mp']>0 else "",str(stats['mp'])))
    #additional effects
    for e in stats['effects']:
        em.add_field(name = e, value = get_effect_description(e))
    return em
        
def generate_combined(name,stats):
    em = discord.Embed(title = name + "'s Stats", color = colorEquipment())
    em.add_field(name = "Main Slot", value = capital(stats['0']))
    em.add_field(name = "Armor Slot", value = capital(stats['1']))
    em.add_field(name = "Accessory Slot", value = capital(stats['2']))
    if stats['3'] != "none": em.add_field(name = "Ammo Slot", value = capital(stats['3']))

    #apply multipliers
    for s in ['pdmg','bdmg','doc','fp']:
        if stats[s] != -1: stats[s] *= stats[s+'-m']
    #toc
    stats['toc'] = -1
    if stats['doc'] > 100:
        stats['toc'] = stats['doc'] - 100
        stats['doc'] = 100
    #-1 stats
    attr = [("Piercing Damage","pdmg"),("Blunt Damage","bdmg"),("Mining Tier","tier"),("Double Ore Chance","doc"),("Triple Ore Chance","toc"),("Fishing Power","fp"),("Line Break Chance","lbc"),("Bait Consumption Chance","bcc"),("Special Drop Chance","sdc"),("Ammo Consumption Chance","acc"),("Main Durability","dur0"),("Armor Durability","dur1"),("Accessory Durability","dur2")]
    for n,i in attr:
        if stats[i] != -1: em.add_field(name = n, value = round(stats[i]))
    #0 stats
    attr = [("Max Health","mhp"),("Defense","def"),("Speed","spd"),("Regeneration","reg")]
    for n,i in attr:
        if stats[i] != 0: em.add_field(name = n, value = round(stats[i]))
    #string stats
    attr = [("Special Drop","drop")]
    for n,i in attr:
        if stats[i] != 'None': em.add_field(name = n, value = stats[i])
    #move priority    
    if stats['mp'] != 0: em.add_field(name = 'Move Priority', value = "{}{}".format("+" if stats['mp']>0 else "",str(stats['mp'])))
    #additional effects
    for e in stats['effects']:
        em.add_field(name = e, value = get_effect_description(e))
    
    return em

def get_stats(user):
    stats = {}
    open_account(user)
    users = getUsers()
    equipment = users[str(user.id)]["equipment"]
    stats['0'] = format(equipment[0])
    if stats['0'] == 'none': stats['0']='fist'
    stats['1'] = format(equipment[1])
    stats['2'] = format(equipment[2])
    stats['3'] = format(equipment[3])
    
    #inits
    for s in ['pdmg','bdmg','tier','doc','fp','lbc','bcc','sdc','acc','dur0','dur1','dur2','dur3']:
        stats[s] = -1
    for s in ['pdmg-m','bdmg-m','doc-m','fp-m']: #multipliers
        stats[s] = 1
    stats['mhp'] = 300
    for s in ['def','spd','mp','reg','critchance']: #zeroes
        stats[s] = 0
    stats['effects'] = []
    stats['drop'] = 'None'
    
    #gather data
    if get_item_category(stats['0']) == "pickaxe":
        stats['tier'] = get_pickaxe_tier(stats['0'])
        stats['doc'] = get_pickaxe_doc(stats['0'])
        stats['dur0'] = get_pickaxe_dur(stats['0'])
    elif get_item_category(stats['0']) == "rod":
        stats['fp'] = get_rod_fp(stats['0'])
        stats['lbc'] = get_rod_lbc(stats['0'])
        stats['bcc'] = get_rod_bcc(stats['0'])
        stats['dur0'] = get_rod_dur(stats['0'])
        if get_item_category(stats['3']) == "bait":
            stats['fp'] += get_bait_fp(stats['3'])
            stats['drop'] = get_bait_drop(stats['3'])
            if stats['drop'] != "None": stats['sdc'] = 3
            stats['effects'] += get_bait_effects(stats['3'])
        else:
            stats['fp'] = -1
            stats['lbc'] = -1
            stats['bcc'] = -1
            stats['dur0'] = -1
    elif get_item_category(stats['0']) == "weapon" or stats['0'] == 'fist':
        stats['pdmg'] = get_weapon_pdmg(stats['0'])
        stats['bdmg'] = get_weapon_bdmg(stats['0'])
        stats['dur0'] = get_weapon_dur(stats['0'])
        stats['effects'] += get_weapon_effects(stats['0'])
        for weapon,ammo in [("Bow","arrow"),("Rocket Launcher","rocket"),("Star Launcher","cometfragment")]:
            if weapon in stats['effects']:
                if get_item_category(stats['3']) == ammo:
                    if (dmg := get_ammo_pdmg(stats['3'])) != -1:
                        if stats['pdmg'] != -1: stats['pdmg'] += dmg
                        else: stats['pdmg'] = dmg
                    if (dmg := get_ammo_bdmg(stats['3'])) != -1:
                        if stats['bdmg'] != -1: stats['bdmg'] += dmg
                        else: stats['bdmg'] = dmg
                    stats['effects'] += get_ammo_effects(stats['3'])
                    stats['acc'] = 100
                else:
                    stats['pdmg'] = -1
                    stats['bdmg'] = -1
                    stats['dur0'] = -1
                    break
    if get_item_category(stats['1']) == "armor":
        stats['def'] = get_armor_def(stats['1'])
        stats['dur1'] = get_armor_dur(stats['1'])
        stats['effects'] += get_armor_effects(stats['1'])
    if get_item_category(stats['2']) == "accessory":
        stats['dur2'] = get_accessory_dur(stats['2'])
        stats['effects'] += get_accessory_effects(stats['2'])
    if users[str(user.id)]["energy"]>0: stats['spd'] = min(math.floor(50*math.log(users[str(user.id)]["energy"],10)),300)
    
    #fully processed effects
    while (effect := 'Bow') in stats['effects']:
        stats['effects'].remove(effect)
    while (effect := 'Rocket Launcher') in stats['effects']:
        stats['effects'].remove(effect)
    while (effect := 'Star Launcher') in stats['effects']:
        stats['effects'].remove(effect)
    while (effect := 'Goes First') in stats['effects']:
        stats['effects'].remove(effect)
        stats['mp'] += 1
    while (effect := 'Goes Last') in stats['effects']:
        stats['effects'].remove(effect)
        stats['mp'] -= 1
    while (effect := 'Always Goes First') in stats['effects']:
        stats['effects'].remove(effect)
        stats['mp'] += 2
    while (effect := 'Always Goes Last') in stats['effects']:
        stats['effects'].remove(effect)
        stats['mp'] -= 2
    while (effect := 'Really Always Goes Last') in stats['effects']:
        stats['effects'].remove(effect)
        stats['mp'] = -100 #just to make it nicer, its after all other priorities, so yeah
    while (effect := 'Critical Chance') in stats['effects']:
        stats['effects'].remove(effect)
        stats['critchance'] += 20
    while (effect := 'Light Weight') in stats['effects']:
        stats['effects'].remove(effect)
        stats['spd'] += 20
    while (effect := 'Raw Power') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['pdmg'] != -1:
            if stats['bdmg'] != -1:
                if stats['pdmg'] + stats['bdmg'] < 200:
                    if stats['pdmg'] > stats['bmdg']: stats['pdmg'] = 200 - stats['bdmg']
                    elif stats['bdmg'] > stats['pmdg']: stats['bdmg'] = 200 - stats['pdmg']
                    else:
                        stats['pdmg'] = 100
                        stats['bdmg'] = 100
                else:
                    stats['pdmg'] += 25
                    stats['bdmg'] += 25
            else:
                if stats['pdmg'] < 200: stats['pdmg'] = 200
                else: stats['pdmg'] += 50
        elif stats['bdmg'] != -1:
            if stats['bdmg'] < 200: stats['bdmg'] = 200
            else: stats['bdmg'] += 50
    while (effect := 'Thorns Damage') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['pdmg'] != -1:
            if stats['bdmg'] != -1:
                stats['pdmg'] += 15
                stats['bdmg'] += 15
            else: stats['pdmg'] += 30
        elif stats['bdmg'] != -1: stats['bdmg'] += 30
    while (effect := 'Ranger') in stats['effects']:
        stats['effects'].remove(effect)
        if get_item_category(format(equipment[3])) in ['rocket','arrow']:
            if stats['pdmg'] != -1:
                if stats['bdmg'] != -1:
                    stats['pdmg'] += 20
                    stats['bdmg'] += 20
                else: stats['pdmg'] += 40
            elif stats['bdmg'] != -1: stats['bdmg'] += 40
    while (effect := 'Slash') in stats['effects']:
        stats['effects'].remove(effect)
        stats['pdmg-m'] *= 1.2
    while (effect := 'More Health') in stats['effects']:
        stats['effects'].remove(effect)
        stats['mhp'] += 100
    while (effect := 'Prickly Shield') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['pdmg'] != -1:
            if stats['bdmg'] != -1:
                stats['pdmg'] += 40
                stats['bdmg'] += 40
            else: stats['pdmg'] += 80
        elif stats['bdmg'] != -1: stats['bdmg'] += 80
        stats['def'] += 125
    while (effect := 'Weakly Buffed') in stats['effects']:
        stats['effects'].remove(effect)
        for s in ['pdmg','bdmg','mhp','def','spd','doc','fp']:
            if stats[s] != -1: stats[s] += 30
    while (effect := 'Buffed') in stats['effects']:
        stats['effects'].remove(effect)
        for s in ['pdmg','bdmg','mhp','def','spd','doc','fp']:
            if stats[s] != -1: stats[s] += 60
    while (effect := 'Strongly Buffed') in stats['effects']:
        stats['effects'].remove(effect)
        for s in ['pdmg','bdmg','mhp','def','spd','doc','fp']:
            if stats[s] != -1: stats[s] += 90
    while (effect := 'Hooked On') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['pdmg'] != -1:
            if stats['bdmg'] != -1:
                stats['pdmg'] += 15
                stats['bdmg'] += 15
            else: stats['pdmg'] += 30
        elif stats['bdmg'] != -1: stats['bdmg'] += 30
        stats['spd'] += 170
    while (effect := 'Strength') in stats['effects']:
        stats['effects'].remove(effect)
        stats['pdmg-m'] *= 1.5
        stats['bdmg-m'] *= 1.5
    while (effect := 'Turtled') in stats['effects']:
        stats['effects'].remove(effect)
        stats['def'] *= 3
        stats['spd'] *= 0.5
        stats['pdmg-m'] *= 0.5
        stats['bdmg-m'] *= 0.5
    while (effect := 'Beetled') in stats['effects']:
        stats['effects'].remove(effect)
        stats['def'] *= 2
        stats['spd'] *= 0.5
    while (effect := 'Cactusificated') in stats['effects']:
        stats['effects'].remove(effect)
        stats['pdmg-m'] *= 2
    while (effect := 'Ironified') in stats['effects']:
        stats['effects'].remove(effect)
        stats['def'] *= 1.25
        stats['pdmg-m'] *= 1.5
    while (effect := 'Lucky') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['doc'] != -1: stats['doc'] += 20
        if stats['bcc'] != -1: stats['bcc'] -= 25
        if stats['lbc'] != -1: stats['lbc'] -= 5
        if stats['sdc'] != -1: stats['sdc'] += 2
    while (effect := 'Fishing Boost') in stats['effects']:
        stats['effects'].remove(effect)
        stats['fp-m'] *= 1.25
        if stats['bcc'] != -1: stats['bcc'] -= 25
        if stats['sdc'] != -1: stats['sdc'] += 2
    while (effect := 'Mining Boost') in stats['effects']:
        stats['effects'].remove(effect)
        stats['doc-m'] *= 1.25
    while (effect := 'Starlight') in stats['effects']:
        stats['effects'].remove(effect)
        stats['doc-m'] *= 1.25
        stats['fp-m'] *= 1.2
        if stats['bcc'] != -1: stats['bcc'] -= 30
        if stats['sdc'] != -1: stats['sdc'] += 5
    while (effect := 'Evil') in stats['effects']:
        stats['effects'].remove(effect)
        stats['pdmg-m'] *= 1.25
        stats['bdmg-m'] *= 1.75
    while (effect := 'Hard') in stats['effects']:
        stats['effects'].remove(effect)
        stats['def'] += 100
    while (effect := 'Light Speed') in stats['effects']:
        stats['effects'].remove(effect)
        stats['spd'] += 500
    while (effect := 'Blessed') in stats['effects']:
        stats['effects'].remove(effect)
        stats['mhp'] += 100
        stats['reg'] += 50
    while (effect := 'Tough') in stats['effects']:
        stats['effects'].remove(effect)
        stats['mhp'] += 50
        stats['def'] += 100
    while (effect := 'Golden') in stats['effects']:
        stats['effects'].remove(effect)
        stats['mhp'] -= 50
        stats['def'] += 50
        if stats['pdmg'] != -1:
            if stats['bdmg'] != -1:
                stats['pdmg'] += 50
                stats['bdmg'] += 50
            else: stats['pdmg'] += 100
        elif stats['bdmg'] != -1: stats['bdmg'] += 100
    while (effect := 'Wall') in stats['effects']:
        stats['effects'].remove(effect)
        stats['def'] += 200
    while (effect := 'Fishing Buff') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['fp'] != -1: stats['fp'] += 25
    while (effect := 'Strong Fishing Buff') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['fp'] != -1: stats['fp'] += 50
    while (effect := 'Mining Buff') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['doc'] != -1: stats['doc'] += 10
    while (effect := 'Strong Mining Buff') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['doc'] != -1: stats['doc'] += 25
    while (effect := 'Silky') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['lbc'] != -1: stats['lbc'] = 0
    
    #partially processed effects
    n = 0
    while (effect := 'Heal Up') in stats['effects']:
        stats['effects'].remove(effect)
        stats['pdmg-m'] *= 0.75
        stats['bdmg-m'] *= 0.75
        n+=1
    for _ in range(n): stats['effects'].append(effect)
    
    #fully processed effects that depend on other stats
    while (effect := 'Regenerator') in stats['effects']:
        stats['effects'].remove(effect)
        stats['reg'] += stats['mhp']/2
    while (effect := 'Speed Boost') in stats['effects']:
        stats['effects'].remove(effect)
        if stats['pdmg'] != -1:
            if stats['bdmg'] != -1:
                stats['pdmg'] += stats['spd'] * 0.25
                stats['bdmg'] += stats['spd'] * 0.25
            else: stats['pdmg'] += stats['spd'] * 0.5
        elif stats['bdmg'] != -1: stats['bdmg'] += stats['spd'] * 0.5
    while (effect := 'Even Out') in stats['effects']:
        stats['effects'].remove(effect)
        stats['def'] *= 0.5
        if stats['pdmg'] != -1:
            if stats['bdmg'] != -1:
                stats['pdmg'] += stats['def'] * 0.5
                stats['bdmg'] += stats['def'] * 0.5
            else: stats['pdmg'] += stats['def']
        elif stats['bdmg'] != -1: stats['bdmg'] += stats['def']
    
    #partially processed effects that depend on other stats
    
    #magic
    if 'Magic' in stats['effects'] and not 'Mana' in stats['effects']:
        stats['pdmg'] = -1
        stats['bdmg'] = -1
        stats['pdmg-m'] = 1
        stats['bdmg-m'] = 1
    
    #final rounding and stuff
    for s in ['def','spd']: #min of 0
        if stats[s] < 0: stats[s] = 0
    for s in ['mhp']: #min of 1
        if stats[s] < 1: stats[s] = 1
    for s in ['acc','bcc']: #min of 5
        if stats[s] < 5 and stats[s] != -1: stats[s] = 5
    for s in ['doc','lbc']: #min of 0
        if stats[s] < 0 and stats[s] != -1: stats[s] = 0
    for s in ['pdmg','bdmg','fp']: #if 0 or negative then disable
        if stats[s] < 1 and stats[s] != -1: stats[s] = -1
    for s in ['tier']: #if negative then disable
        if stats[s] < 0 and stats[s] != -1: stats[s] = -1
    for s in ['pdmg','bdmg','tier','doc','fp','lbc','bcc','acc','mhp','def','spd','mp','dur0','dur1','dur2','dur3','critchance','reg']: #rounding stats
        stats[s] = round(stats[s])
    for s in ['pdmg-m','bdmg-m','doc-m','fp-m']: #rounding multipliers
        stats[s] = round(stats[s],2) #2dp
    stats['hp'] = stats['mhp']
    return stats











### ITEMS ###

def get_rarity(power=100):
    def item_chance(base,peak,minimum,power): # determines percentage odds
        if power < minimum: return 0
        if power > 500: return peak
        if power < 100: return base
        return base + (power-100)*(peak-base)/400
    veryrare,rare,uncommon = item_chance(1,5,100,power),item_chance(10,20,75,power),item_chance(30,60,0,power) # gets percentage odds
    rando = random.randrange(0,100) # gets rarity based on odds
    rarity = 'Common'
    if rando < veryrare: rarity = 'Very Rare'
    elif rando < veryrare+rare: rarity = 'Rare'
    elif rando < veryrare+rare+uncommon: rarity = 'Uncommon'
    return rarity












### MAP ###

def get_location(user):
    users = getUsers()
    try:
        location = users[str(user.id)]["location"]
        locationinfo = getMap()['locations'][format(location)]
    except:
        return (-1,0,False,False,False,{})
    air = locationinfo['air']
    stats = get_stats(user)
    status = 0
    if not 'Wings' in stats['effects'] and air:
        try:
            air = False
            location = "skycity"
            users[str(user.id)]["location"] = location
            locationinfo = getMap()['locations'][location]
            writeUsers()
            status = 1
        except:
            return (-1,0,False,False,False,{})
    safety = 1
    if locationinfo['conflict'] == "safe": safety = 2
    elif locationinfo['conflict'] == "foreign": safety = 0
    controlled = locationinfo['controller'] == "Blue Republic"
    lava = locationinfo['lava']
    return status,safety,controlled,air,lava,locationinfo
    
def generate_map_1(data):
    em = discord.Embed(title = f"{data['name']} (1/5): General", color = colorMap(), description = data['description'])
    em.add_field(name="Controller",value=data['controller'])
    val = "Currently safe, why not visit!"
    match data['conflict']:
        case 'fighting':
            val = "Some fighting going on, you can join in but if you want to visit maybe wait until another time."
        case 'fightingbattle':
            val = "Some fighting and a battle going on, you can join in but if you want to visit maybe wait until another time."
        case 'battle':
            val = "A battle is going on, you can join in but if you want to visit maybe wait until another time."
        case 'foreign':
            val = "Who knows what's going on here, you cannot travel to a foreign land."
    em.add_field(name="Current State",value=val)
    if data['lava']: em.add_field(name="Lava",value="There is lava here, so you will need special equipment to fish.")
    if data['air']: em.add_field(name="Air",value="This place is in the sky, so you will need special equipment to travel here.")
    return em
    
def generate_map_2(data):
    em = discord.Embed(title = f"{data['name']} (2/5): Resources", color = colorMap(), description = data['description'])
    em.add_field(name="Sun",value=data['sun'])
    em.add_field(name="Wind",value=data['wind'])
    for r,a in data['resources'].items():
        if isinstance(a,list): val = "-".join([str(k) for k in a])
        else: val = str(a)
        em.add_field(name=r,value=val)
    return em
    
def generate_map_3(data):
    em = discord.Embed(title = f"{data['name']} (3/5): Mobs", color = colorMap(), description = data['description'])
    for r in ["Common","Uncommon","Rare","Very Rare"]:
        em.add_field(name=r,value=", ".join(data['fighting'][r]))
    return em
    
def generate_map_4(data):
    em = discord.Embed(title = f"{data['name']} (4/5): Fishing", color = colorMap(), description = data['description'])
    for r in ["Common","Uncommon","Rare","Very Rare"]:
        em.add_field(name=r,value=", ".join(["{} {}".format("-".join([str(k) for k in a]) if isinstance(a,list) else str(a),i) for i,a in data['fishing'][r].items()]))        
    return em
    
def generate_map_5(data):
    em = discord.Embed(title = f"{data['name']} (5/5): Mining", color = colorMap(), description = data['description'])
    for r,a in data['mining']['Ore'].items():
        em.add_field(name=r,value=f"{a} Rarity")
    for r in ["Common","Uncommon","Rare","Very Rare"]:
        em.add_field(name=r,value=", ".join(["{} {}".format("-".join([str(k) for k in a]) if isinstance(a,list) else str(a),i) for i,a in data['mining'][r].items()]))        
    return em










### MINING ###

def mine_this(mininginfo,oresinfo,tier,doc,dur,item=False):
    ores = {}
    amt = 0
    drop = ""
    rarity = ""
    for ore,rari in mininginfo['Ore'].items():
        obti = getAtTier(tier,ore,oresinfo)
        thisore = 0
        if obti > 0:
            thisore = random.randrange(-rari,2)
            if thisore < 0: thisore=0
            if thisore > 0 and obti > 1 and percentage_chance(doc): thisore=2 #double ore chance
            if thisore > 0 and obti > 1 and percentage_chance(doc-100): thisore=3 #triple ore chance
        if thisore > 0: ores[ore] = thisore
    if item:
        rarity = get_rarity()
        drop = random.choice(list(mininginfo[rarity].keys()))
        amt = parse_number(mininginfo[rarity][drop])
    return (reciprocal_chance(dur),ores,amt,drop,rarity)

def getAtTier(tier,ore=-1,ores=-1):
    if ores == -1:ores = getOres()
    if ore == -1:
        normal = []; reduced = []
        for ore,data in ores.items():
            if tier >= data['tier']: normal.append(data['name'])
            elif tier >= data['reducedtier']: reduced.append(data['name'])
        return (normal,reduced)
    if not format(ore) in ores.keys(): return 1
    if tier >= ores[format(ore)]['tier']: return 2
    if tier >= ores[format(ore)]['reducedtier']: return 1
    return 0








### FIGHTING ###

def weaponsuitability(item):
    item = format(item)
    banned = getBanned()
    
    if item in banned['godlike']: return 4
    if item in banned['overpowered']: return 3
    if item in banned['inappropriate']: return 2
    
    random.seed(date.today().isocalendar().week)
    dailychoices = random.sample(banned['weaponchoices'],k=15) # allows 15 out of 30 weapons
    random.seed()
    
    if not item in dailychoices: return 1
    return -1

def armorsuitability(item):
    item = format(item)
    banned = getBanned()
    
    if item in banned['godlike']: return 4
    if item in banned['overpowered']: return 3
    if item in banned['inappropriate']: return 2
    
    random.seed(date.today().isocalendar().week)
    dailychoices = random.sample(banned['armorchoices'],k=5) # allows 5 out of 10 armor pieces
    random.seed()
    
    if not item in dailychoices: return 1
    return -1

def accessorysuitability(item):
    item = format(item)
    banned = getBanned()
    
    if item in banned['godlike']: return 4
    if item in banned['overpowered']: return 3
    if item in banned['inappropriate']: return 2
    
    return -1

def ammosuitability(item):
    item = format(item)
    banned = getBanned()
    
    if item in banned['godlike']: return 4
    if item in banned['overpowered']: return 3
    if item in banned['inappropriate']: return 2
    
    return -1

def fight_between(astats,bstats,aname,bname):
    # one turn
    def fight_turn(attacker,defender,firstmove:bool,logs):
        # starting turn
        hits = 1
        basepdmg,basebdmg,basepdmgm,basebdmgm = attacker['pdmg'],attacker['bdmg'],attacker['pdmg-m'],attacker['bdmg-m']
        if 'Fragile' in attacker['effects'] and defender['def'] >= 300: attacker['broke0'] = True
        if 'Breakable' in defender['effects']:
            enemydmg = 0
            if attacker['pdmg'] != -1: enemydmg += attacker['pdmg'] * attacker['pdmg-m']
            if attacker['bdmg'] != -1: enemydmg += attacker['bdmg'] * attacker['bdmg-m']
            if enemydmg >= 300: defender['broke2'] = True
        if 'Elastic Potential' in attacker['effects'] and attacker['dmgtaken'] > 0:
            if attacker['pdmg'] != -1:
                if attacker['bdmg'] != -1:
                    attacker['pdmg'] += attacker['dmgtaken']
                    attacker['bdmg'] += attacker['dmgtaken']
                else: attacker['pdmg'] += attacker['dmgtaken'] * 2
            elif attacker['bdmg'] != -1: attacker['bdmg'] += attacker['dmgtaken'] * 2
        if 'Surprise' in attacker['effects'] and firstmove:
            attacker['pdmg-m'] *= 3;attacker['bdmg-m'] *= 3
        if 'Double Hit' in attacker['effects']: hits += 1
        if 'Multi Hit' in attacker['effects']: hits += random.randrange(0,5)
        
        # the actual fighting lmao
        dmg = 0
        ignoredefense = 'Magic' in attacker['effects'] and 'Mana' in attacker['effects']
        if percentage_chance(attacker['critchance']): ignoredefense = True
        if attacker['pdmg'] != -1:
            attacker['pdmg'] *= attacker['pdmg-m']
            if not ignoredefense:
                if 'Sharp' in attacker['effects']:
                    defender['def'] -= 50
                    if defender['def'] > 0: attacker['pdmg'] -= defender['def']
                    defender['def'] += 50
                elif defender['def'] > 0: attacker['pdmg'] -= defender['def']
                if attacker['pdmg'] < 0: attacker['pdmg'] = 0
            dmg += attacker['pdmg']
        if attacker['bdmg'] != -1:
            attacker['bdmg'] *= attacker['bdmg-m']
            if 'Dense' in defender['effects']:
                attacker['bdmg'] -= 50
                if attacker['bdmg'] < 0: attacker['bdmg'] = 0
            dmg += attacker['bdmg']
        if 'Defense Basher' in attacker['effects']: dmg += defender['def'] * 0.5
        logs.append("{} dealt {} damage to {}.".format(attacker['name'],dmg,defender['name']))
        if not ignoredefense and defender['def'] > 0:
            defender['def'] -= dmg
            if defender['def'] < 0:
                dmg = -defender['def']
                defender['def'] = 0
            else: dmg = 0
        if 'Withering' in attacker['effects']:
            dmg += 100
            logs.append("{} suffered 100 damage due to Withering.".format(defender['name']))
        defender['hp'] -= dmg
        if defender['hp'] < 0: defender['hp'] = 0
        
        # ending turn
        attacker['pdmg'],attacker['bdmg'],attacker['pdmg-m'],attacker['bdmg-m'] = basepdmg,basebdmg,basepdmgm,basebdmgm
        if 'Power Up' in attacker['effects']:
            attacker['pdmg-m'] *= 2;attacker['bdmg-m'] *= 2
            logs.append("{} is powering up.".format(attacker['name']))
        reg = defender['reg']
        if 'Heal Up' in defender['effects'] and defender['hp'] > defender['mhp']*0.3: reg += defender['mhp'] - defender['hp']
        if reg + defender['hp'] > defender['mhp']: reg = defender['mhp'] - defender['hp']
        if reg > 0:
            defender['hp'] += reg
            logs.append("{} regenerated {} hp.".format(defender['name'],reg))

    # set up
    astats['broke0'] = reciprocal_chance(astats['dur0']);bstats['broke0'] = reciprocal_chance(bstats['dur0'])
    astats['broke1'] = reciprocal_chance(astats['dur1']);bstats['broke1'] = reciprocal_chance(bstats['dur1'])
    astats['broke2'] = reciprocal_chance(astats['dur2']);bstats['broke2'] = reciprocal_chance(bstats['dur2'])
    astats['broke3'] = percentage_chance(astats['acc']);bstats['broke3'] = percentage_chance(bstats['acc'])
    astats['dmgtaken'] = 0;bstats['dmgtaken'] = 0
    astats['status'] = 'Fine';bstats['status'] = 'Fine'
    astats['name'] = aname;bstats['name'] = bname
    logs = []
    
    while (effect := 'Soothing') in astats['effects']:
        astats['effects'].remove(effect)
        bstats['pdmg-m'] *= 0.5
        bstats['bdmg-m'] *= 0.5
    while (effect := 'Soothing') in bstats['effects']:
        bstats['effects'].remove(effect)
        astats['pdmg-m'] *= 0.5
        astats['bdmg-m'] *= 0.5
    while (effect := 'Deep Dark') in astats['effects']:
        astats['effects'].remove(effect)
        bstats['spd'] *= 0.5
    while (effect := 'Deep Dark') in bstats['effects']:
        bstats['effects'].remove(effect)
        astats['spd'] *= 0.5
    while (effect := 'Counter Magic') in astats['effects']:
        astats['effects'].remove(effect)
        if 'Mana' in bstats['effects']:
            astats['pdmg-m'] *= 0.5
            astats['bdmg-m'] *= 0.5
    while (effect := 'Counter Magic') in bstats['effects']:
        bstats['effects'].remove(effect)
        if 'Mana' in astats['effects']:
            bstats['pdmg-m'] *= 0.5
            bstats['bdmg-m'] *= 0.5
    while (effect := 'Magic Guard') in astats['effects']:
        astats['effects'].remove(effect)
        if 'Magic' in bstats['effects']:
            bstats['pdmg-m'] *= 0.5
            bstats['bdmg-m'] *= 0.5
    while (effect := 'Magic Guard') in bstats['effects']:
        bstats['effects'].remove(effect)
        if 'Magic' in astats['effects']:
            astats['pdmg-m'] *= 0.5
            astats['bdmg-m'] *= 0.5
    
    # partially processed starting fight effects
    n = 0
    while (effect := 'Explosion') in astats['effects']:
        astats['effects'].remove(effect)
        bstats['def'] *= 0.5
        n+=1
    for _ in range(n): astats['effects'].append(effect)
    n = 0
    while (effect := 'Explosion') in bstats['effects']:
        bstats['effects'].remove(effect)
        astats['def'] *= 0.5
        n+=1
    for _ in range(n): bstats['effects'].append(effect)
    
    # fight loop
    moves = 0
    while astats['status'] == 'Fine' and bstats['status'] == 'Fine' and moves < 10:
        for s in ['def','hp','mhp','pdmg','bdmg']:
            astats[s] = int(astats[s])
            bstats[s] = int(bstats[s])
        logs.append("{}: {}{}/{}".format(astats['name'],"{}+".format(astats['def'])if astats['def']>0 else"",astats['hp'],astats['mhp']))
        logs.append("{}: {}{}/{}".format(bstats['name'],"{}+".format(bstats['def'])if bstats['def']>0 else"",bstats['hp'],bstats['mhp']))
        # move order
        ashielded = False;bshielded = False
        if 'Shielded' in astats['effects']:
            enemydmg = 0
            if bstats['pdmg'] != -1: enemydmg += bstats['pdmg'] * bstats['pdmg-m']
            if bstats['bdmg'] != -1: enemydmg += bstats['bdmg'] * bstats['bdmg-m']
            if enemydmg < 500:
                ashielded = True
                astats['mp'] += 10
        if 'Shielded' in bstats['effects']:
            enemydmg = 0
            if astats['pdmg'] != -1: enemydmg += astats['pdmg'] * astats['pdmg-m']
            if astats['bdmg'] != -1: enemydmg += astats['bdmg'] * astats['bdmg-m']
            if enemydmg < 500:
                bshielded = True
                bstats['mp'] += 10
        if astats['mp']>bstats['mp'] or astats['mp']==bstats['mp'] and astats['spd']>=bstats['spd']:
            first = astats; last = bstats
        else:
            first = bstats; last = astats
        if ashielded:astats['mp'] -= 10
        if bshielded:bstats['mp'] -= 10
        # first's turn
        if not ('Block' in last['effects'] and moves==0):
            fight_turn(first,last,True,logs)
            if first['hp'] <= 0: first['status'] = 'Dead'
            elif first['hp'] <= 0.3*first['mhp']: first['status'] = 'KO'
            if last['hp'] <= 0: last['status'] = 'Dead'
            elif last['hp'] <= 0.3*last['mhp']: last['status'] = 'KO'
            if first['status'] == 'Dead' or last['status'] == 'Dead': break
        # last's turn
        if not ('Block' in first['effects'] and moves==0):
            fight_turn(last,first,False,logs)
            if first['hp'] <= 0: first['status'] = 'Dead'
            elif first['hp'] <= 0.3*first['mhp']: first['status'] = 'KO'
            if last['hp'] <= 0: last['status'] = 'Dead'
            elif last['hp'] <= 0.3*last['mhp']: last['status'] = 'KO'
            if first['status'] == 'Dead' or last['status'] == 'Dead': break
        # ending
        if 'Explosion' in astats['effects']:
            if astats['status'] == 'Fine': astats['status'] = 'Exploded' # explodes, ending the fight
        if 'Explosion' in bstats['effects']:
            if bstats['status'] == 'Fine': bstats['status'] = 'Exploded' # explodes, ending the fight
        moves += 1
    
    logs.append("{}: {}{}/{}".format(astats['name'],"{}+".format(astats['def'])if astats['def']>0 else"",astats['hp'],astats['mhp']))
    logs.append("{}: {}{}/{}".format(bstats['name'],"{}+".format(bstats['def'])if bstats['def']>0 else"",bstats['hp'],bstats['mhp']))
    
    # end of fight
    while (effect := 'Sacrificial') in astats['effects']:
        astats['effects'].remove(effect)
        if astats['break0']:
            astats['break0'] = False
            astats['break2'] = True
            continue
        if astats['break1']:
            astats['break1'] = False
            astats['break2'] = True
            continue
    while (effect := 'Sacrificial') in bstats['effects']:
        bstats['effects'].remove(effect)
        if bstats['break0']:
            bstats['break0'] = False
            bstats['break2'] = True
            continue
        if bstats['break1']:
            bstats['break1'] = False
            bstats['break2'] = True
            continue
            
    if 'Magic' in astats['effects'] and 'Mana' in astats['effects']: astats['broke2'] = True
    if 'Magic' in bstats['effects'] and 'Mana' in bstats['effects']: bstats['broke2'] = True
    
    # return
    return {'astatus':astats['status'],'bstatus':bstats['status'],'abroke0':astats['broke0'],'abroke1':astats['broke1'],'abroke2':astats['broke2'],'abroke3':astats['broke3'],'bbroke0':bstats['broke0'],'bbroke1':bstats['broke1'],'bbroke2':bstats['broke2'],'bbroke3':bstats['broke3'],'logs':"\n".join(logs)}


    
def generate_fighting_1(data):
    em = discord.Embed(title = f"{data['name']} {data['type']} (1/3): Stats", color = colorInfo(), description = data['description'])
    for s,n in [('pdmg','Piercing'),('bdmg','Blunt'),('mhp','Health'),('def','Defense'),('spd','Speed')]:
        if data[s] != -1: em.add_field(name=n,value=data[s])
    for e in data['effects']:
        em.add_field(name=e,value=get_effect_description(e))
    return em

def generate_fighting_2(data):
    em = discord.Embed(title = f"{data['name']} {data['type']} (2/3): Drops", color = colorInfo(), description = data['description'])
    for r in ["Common","Uncommon","Rare","Very Rare"]:
        em.add_field(name=r,value=", ".join(["{} {}".format("-".join([str(k) for k in a]) if isinstance(a,list) else str(a),i) for i,a in data['drops'][r].items()]))        
    return em

def generate_fighting_3(data):
    em = discord.Embed(title = f"{data['name']} {data['type']} (3/3): Locations", color = colorInfo(), description = data['description'])
    locations = {}
    for l,d in getMap()['locations'].items():
        for r in ["Common","Uncommon","Rare","Very Rare"]:
            if data['name'] in d['fighting'][r]:
                if r in list(locations.keys()): locations[r].append(d['name'])
                else: locations[r] = [d['name']]
    for r in ["Common","Uncommon","Rare","Very Rare"]:
        if r in list(locations.keys()): em.add_field(name=r,value=", ".join(locations[r]))     
    return em











### FISHING ###

def fish_this(fishinginfo,fp,lbc,bcc,dur):
    rarity = get_rarity(fp)
    drop = random.choice(list(fishinginfo[rarity].keys()))
    amt = parse_number(fishinginfo[rarity][drop])
    return (reciprocal_chance(dur),percentage_chance(lbc),percentage_chance(bcc),amt,drop,rarity)













### STALLS ###

def addstall(user,stallid,item,price,slogan,gangonly):
    users = getUsers()
    try:
        users[str(user.id)]["stalls"][stallid] = [item,price,slogan,gangonly,0]
    except:
        users[str(user.id)]["stalls"] = {stallid:[item,price,slogan,gangonly,0]}
    writeUsers()

def updatestall(owner,stallid,stall):
    users = getUsers()
    try:
        users[owner]["stalls"][stallid] = stall
    except:
        users[owner]["stalls"] = {stallid:stall}
    writeUsers()

def removestall(user,stallid):
    users = getUsers()
    try:
        addtobag(user,users[str(user.id)]["stalls"][stallid][0],users[str(user.id)]["stalls"][stallid][4])
        users[str(user.id)]["stalls"].pop(stallid)
        writeUsers()
    except:
        return -1

def getstalls(user):
    users = getUsers()
    try:
        return users[str(user.id)]["stalls"]
    except:
        return {}

def getallstalls(user):
    users = getUsers()
    stalls = {}
    for i,z in users.items():
        if not haseitherboycott(i,user.id) and "stalls" in list(z.keys()):
            for n,s in z["stalls"].items():
                if not s[3] or users[i]["gang"] == "None" or users[i]["gang"] == users[str(user.id)]["gang"]:
                    stalls[n] = s
    return stalls

def getstall(user,stallid):
    users = getUsers()
    try:
        return users[str(user.id)]["stalls"][stallid]
    except:
        return None

def hasstall(user,stallid):
    users = getUsers()
    try:
        users[str(user.id)]["stalls"][stallid]
        return True
    except:
        return False

def findstall(item,amount,finderid,personid):
    finderid = str(finderid)
    personid = str(personid)
    users = getUsers()
    stalls = {}
    for i,z in users.items():
        if personid == "" or i == personid: 
            if not haseitherboycott(i,finderid) and "stalls" in list(z.keys()):
                for n,s in z["stalls"].items():
                    if not s[3] or users[i]["gang"] == "None" or users[i]["gang"] == users[finderid]["gang"]:
                        if format(s[0]) == format(item) and s[4] >= amount:
                            stalls[n] = (i,n,s)
    print("stalls:",stalls)
    stall = (None,None,None)
    if len(stalls) > 0:
        for n,z in stalls.items():
            if stall[2] == None or z[2][1] < stall[2][1]: stall = z
    return stall
    

def toggleboycott(user,boycottid):
    boycottid = str(boycottid)
    users = getUsers()
    if "boycotts" in list(users[str(user.id)].keys()) and boycottid in users[str(user.id)]["boycotts"]:
        users[str(user.id)]["boycotts"].remove(str(boycottid))
    else:
        try:
            users[str(user.id)]["boycotts"].append(str(boycottid))
        except:
            users[str(user.id)]["boycotts"] = [str(boycottid)]
    writeUsers()

def hasboycott(user,boycottid):
    boycottid = str(boycottid)
    users = getUsers()
    return "boycotts" in list(users[str(user.id)].keys()) and boycottid in users[str(user.id)]["boycotts"]

def haseitherboycott(user1id,user2id):
    user1id = str(user1id)
    user2id = str(user2id)
    users = getUsers()
    return "boycotts" in list(users[user1id].keys()) and user2id in users[user1id]["boycotts"] or "boycotts" in list(users[user2id].keys()) and user1id in users[user2id]["boycotts"]

def getboycotts(user):
    users = getUsers()
    try:
        return users[str(user.id)]["boycotts"]
    except:
        return {}
















### PLOTS ###
    
def addplots(user,plot,amount=1):
    users = getUsers()
    plot = format(plot)
    resourcesMap = getMap()["locations"][plot]["resources"]
    resources = {}
    for k,v in resourcesMap.items():
        resources[k] = sum([parse_number(v) for _ in range(amount)])
    try:
        users[str(user.id)]["plots"][plot]["number"] += amount
        for resource,num in resources:
            users[str(user.id)]["plots"][plot]["resources"][resource] += num
    except:
        try:
            users[str(user.id)]["plots"][plot] = {"number":amount,"resources":resources,"machines":{}}
        except:
            users[str(user.id)]["plots"] = {plot:{"number":amount,"resources":resources,"machines":{}}}
    writeUsers()

def valid_plot(plot_name):
    try:
        data = getMap()['locations'][format(plot_name)]
    except:
        return False
    return True

def valid_machine(machine_name):
    pms = getPlotmachines()
    for k in pms.keys():
        if format(k) == format(item_name):
            return True
    return False

def valid_resource(resource_name):
    resources = getResources()
    for k in resources.keys():
        if format(k) == format(item_name):
            return True
    return False
    
def addplotmachines(user,plot,machine,amount=1):
    users = getUsers()
    plot = format(plot)
    machine = format(machine)
    try:
        users[str(user.id)]["plots"][plot]["machines"][machine] += amount
    except:
        users[str(user.id)]["plots"][plot]["machines"][machine] = amount
    writeUsers()
    
def removeplotmachines(user,plot,machine,amount=1):
    users = getUsers()
    plot = format(plot)
    machine = format(machine)
    users[str(user.id)]["plots"][plot]["machines"][machine] -= amount
    writeUsers()
    
def removeplotresources(user,plot,resource,amount=1):
    users = getUsers()
    plot = format(plot)
    resource = format(resource)
    users[str(user.id)]["plots"][plot]["resources"][resource] -= amount
    writeUsers()
    
def getplots(user):
    users = getUsers()
    try:
        return users[str(user.id)]["plots"]
    except:
        return {}

def getplotnumber(user,plot):
    users = getUsers()
    plot = format(plot)
    try:
        return users[str(user.id)]["plots"][plot]["number"]
    except:
        return 0

def getplotresources(user,plot):
    users = getUsers()
    plot = format(plot)
    try:
        return users[str(user.id)]["plots"][plot]["resources"]
    except:
        return {}

def getplotresource(user,plot,resource):
    users = getUsers()
    plot = format(plot)
    resource = format(resource)
    try:
        return users[str(user.id)]["plots"][plot]["resources"][resource]
    except:
        return 0

def getplotnumresources(user,plot):
    count = 0
    for k,v in getplotnumresources(user,plot).items():
        count += v
    return count

def getplotmachines(user,plot):
    users = getUsers()
    try:
        return users[str(user.id)]["plots"][plot]["machines"]
    except:
        return {}

def getplotmachine(user,plot,machine):
    users = getUsers()
    plot = format(plot)
    machine = format(machine)
    try:
        return users[str(user.id)]["plots"][plot]["machines"][machine]
    except:
        return 0

def getplotnummachines(user,plot):
    count = 0
    for k,v in getplotmachines(user,plot).items():
        count += v
    return count

def collectplotsbyhand(user):
    plots = getplots(user)
    resourcesLimit = getResources()
    resources = {}
    for p in plots.keys():
        if p == "storage":
            continue
        for r in getplotresources(user,p).keys():
            num = getplotresource(user,p,r)
            if num > resourcesLimit[r]: num = resourcesLimit[r]
            removeplotresources(user,p,r,num)
            try:
                resources[r] += num
            except:
                resources[r] = num
    addalltobag(user,resources)
    writeUsers()
    return resources

def collectplotsbymachine(user):
    plots = getplots(user)
    extracted = {}
    consumed = {}
    for p in plots.keys():
        if p == "storage" or not doesplothaveenoughenergy(user,p):
            continue
        resourcesLimit = {}
        for m,num in getplotmachines(user,p).items():
            conditions = True
            for k,v in getPlotmachines()[m]["consumed"].items():
                if k == "battery": #battery : check from bag not from plot resources, and have to check total so far since bag is for everything, order is arbitrary
                    if amountinbag(user,k) < v*num:
                        condition = False
                        break
                elif k == "chargedbattery": #chargedbattery : check from bag not from plot resources, and have to check total so far since bag is for everything, order is arbitrary
                    if amountinbag(user,k) < v*num:
                        condition = False
                        break
                elif getplotresource(p,k) < v*num: #otherwise: just work as normal checking the plot resources
                    condition = False
                    break
            if condition:
                for k,v in getPlotmachines()[m]["consumed"].items():
                    try:
                        consumed[k] += v*num
                    except:
                        consumed[k] = v*num
                    if k == "battery" or k == "chargedbattery": removefrombag(user,k,v*num) # batteries get consumed from bag
                    else: removeplotresources(user,p,k,v*num) # resources get consumed from plot
                for k,v in getPlotmachines()[m]["extracted"].items():
                    try:
                        resourcesLimit[k] += v*num
                    except:
                        resourcesLimit[k] = v*num
        for r in getplotresources(user,p).keys():
            num = getplotresource(user,p,r)
            if num > resourcesLimit[r]: num = resourcesLimit[r]
            removeplotresources(user,p,r,num)
            try:
                extracted[r] += num
            except:
                extracted[r] = num
    addalltobag(user,extracted)
    writeUsers()
    return (extracted,consumed)

def energyproducedbyplot(user):
    plots = getplots(user)
    energies = {}
    batteries = 0
    for p in plots.keys():
        if p == "storage":
            continue
        for m,num in getplotmachines(user,p).items():
            conditions = True
            power = getPlotmachines()[m]["power"]
            if power < 0:
                for k,v in getPlotmachines()[m]["consumed"].items():
                    if k == "sun": #sun : don't consume the non-existent sun item, and multiply power by sun value in the location
                        power *= getMap()["locations"][p]["sun"]
                    elif k == "wind": #wind : don't consume the non-existent wind item, and multiply power by wind value in the location
                        power *= getMap()["locations"][p]["wind"]
                    elif k == "chargedbattery": #chargedbattery : check from bag not from plot resources, and have to check total so far since bag is for everything, order is arbitrary
                        batteries += v*num
                        if amountinbag(user,k) < batteries:
                            condition = False
                            break
                    elif getplotresource(p,k) < v*num: #otherwise: just work as normal checking the plot resources
                        condition = False
                        break
                if conditions:
                    energies[p] = -power
                else:
                    energies[p] = 0
            else:
                energies[p] = 0
    addalltobag(user,resources)
    return energies

def energyconsumedbyplot(user):
    plots = getplots(user)
    energies = {}
    batteries = 0
    for p in plots.keys():
        if p == "storage":
            continue
        for m,num in getplotmachines(user,p).items():
            conditions = True
            power = getPlotmachines()[m]["power"]
            if power > 0:
                for k,v in getPlotmachines()[m]["consumed"].items():
                    if k == "battery": #battery : check from bag not from plot resources, and have to check total so far since bag is for everything, order is arbitrary
                        batteries += v*num
                        if amountinbag(user,k) < batteries:
                            condition = False
                            break
                    elif getplotresource(p,k) < v*num: #otherwise: just work as normal checking the plot resources
                        condition = False
                        break
                if conditions:
                    energies[p] = power
                else:
                    energies[p] = 0
            else:
                energies[p] = 0
    addalltobag(user,resources)
    return energies

def doesplothaveenoughenergy(user,plot):
    if plot == "storage": return True #its skipped anyway when resources are collected, just True so that the need more energy message doesn't display in /plots
    return energyproducedbyplot(user)[plot] >= energyconsumedbyplot(user)[plot]