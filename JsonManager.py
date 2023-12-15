
#---------------------------------------------------------------------------SETUP----------------------------------------------------------------------------------------#

### IMPORTS ###

import json
import io




### GLOBALS ###

_users = None
_items = None
_itemsog = None
_foods = None
_pickaxes = None
_rods = None
_weapons = None
_armor = None
_accessories = None
_ammo = None
_bait = None
_crafting = None
_brewing = None
_banned = None
_ores = None
_mobs = None
_resources = None
_map = None











#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### SPECIAL ###

def refresh():
    global _users, _items, _itemsog, _foods, _pickaxes, _rods, _weapons, _armor, _accessories, _ammo, _bait, _crafting, _brewing, _banned, _ores, _mobs, _resources, _map
    with open("data\\users.json",'r') as f:
        _users = json.load(f)
    with open("data\\items.json",'r') as f:
        _items = json.load(f)
    with open("data\\itemsog.json",'r') as f:
        _itemsog = json.load(f)
    with open("data\\foods.json",'r') as f:
        _foods = json.load(f)
    with open("data\\pickaxes.json",'r') as f:
        _pickaxes = json.load(f)
    with open("data\\rods.json",'r') as f:
        _rods = json.load(f)
    with open("data\\weapons.json",'r') as f:
        _weapons = json.load(f)
    with open("data\\armor.json",'r') as f:
        _armor = json.load(f)
    with open("data\\accessories.json",'r') as f:
        _accessories = json.load(f)
    with open("data\\ammo.json",'r') as f:
        _ammo = json.load(f)
    with open("data\\bait.json",'r') as f:
        _bait = json.load(f)
    with open("data\\crafting.json",'r') as f:
        _crafting = json.load(f)
    with open("data\\brewing.json",'r') as f:
        _brewing = json.load(f)
    with open("data\\banned.json",'r') as f:
        _banned = json.load(f)
    with open("data\\ores.json",'r') as f:
        _ores = json.load(f)
    with open("data\\mobs.json",'r') as f:
        _mobs = json.load(f)
    with open("data\\resources.json",'r') as f:
        _resources = json.load(f)
    with io.open("data\\map.json",mode='r',encoding="utf-16") as f:
        _map = json.load(f)
        
def update():
    global _users, _items, _itemsog, _foods, _pickaxes, _rods, _weapons, _armor, _accessories, _ammo, _bait, _crafting, _brewing, _banned, _ores, _mobs, _resources, _map
    getUsers()
    getItems()
    getItemsOg()
    getFoods()
    getPickaxes()
    getRods()
    getWeapons()
    getArmor()
    getAccessories()
    getAmmo()
    getBait()
    getCrafting()
    getBrewing()
    getBanned()
    getOres()
    getMobs()
    getResources()
    getMap()
    with open("data\\users.json",'w') as f:
        json.dump(_users,f,indent=4,sort_keys=True)
    with open("data\\items.json",'w') as f:
        json.dump(_items,f,indent=4,sort_keys=True)
    with open("data\\itemsog.json",'w') as f:
        json.dump(_itemsog,f,indent=4,sort_keys=True)
    with open("data\\foods.json",'w') as f:
        json.dump(_foods,f,indent=4,sort_keys=True)
    with open("data\\pickaxes.json",'w') as f:
        json.dump(_pickaxes,f,indent=4,sort_keys=True)
    with open("data\\rods.json",'w') as f:
        json.dump(_rods,f,indent=4,sort_keys=True)
    with open("data\\weapons.json",'w') as f:
        json.dump(_weapons,f,indent=4,sort_keys=True)
    with open("data\\armor.json",'w') as f:
        json.dump(_armor,f,indent=4,sort_keys=True)
    with open("data\\accessories.json",'w') as f:
        json.dump(_accessories,f,indent=4,sort_keys=True)
    with open("data\\ammo.json",'w') as f:
        json.dump(_ammo,f,indent=4,sort_keys=True)
    with open("data\\bait.json",'w') as f:
        json.dump(_bait,f,indent=4,sort_keys=True)
    with open("data\\crafting.json",'w') as f:
        json.dump(_crafting,f,indent=4,sort_keys=True)
    with open("data\\brewing.json",'w') as f:
        json.dump(_brewing,f,indent=4,sort_keys=True)
    with open("data\\banned.json",'w') as f:
        json.dump(_banned,f,indent=4,sort_keys=True)
    with open("data\\ores.json",'w') as f:
        json.dump(_ores,f,indent=4,sort_keys=True)
    with open("data\\mobs.json",'w') as f:
        json.dump(_mobs,f,indent=4,sort_keys=True)
    with open("data\\resources.json",'w') as f:
        json.dump(_resources,f,indent=4,sort_keys=True)
    with io.open("data\\map.json",mode='w',encoding="utf-16") as f:
        json.dump(_map,f,indent=4,sort_keys=True)





### GETS ###

def getUsers():
    global _users
    if _users == None:
        with open("data\\users.json",'r') as f:
            _users = json.load(f)
    return _users

def getItems():
    global _items
    if _items == None:
        with open("data\\items.json",'r') as f:
            _items = json.load(f)
    return _items

def getItemsOg():
    global _itemsog
    if _itemsog == None:
        with open("data\\itemsog.json",'r') as f:
            _itemsog = json.load(f)
    return _itemsog

def getFoods():
    global _foods
    if _foods == None:
        with open("data\\foods.json",'r') as f:
            _foods = json.load(f)
    return _foods

def getPickaxes():
    global _pickaxes
    if _pickaxes == None:
        with open("data\\pickaxes.json",'r') as f:
            _pickaxes = json.load(f)
    return _pickaxes

def getRods():
    global _rods
    if _rods == None:
        with open("data\\rods.json",'r') as f:
            _rods = json.load(f)
    return _rods

def getWeapons():
    global _weapons
    if _weapons == None:
        with open("data\\weapons.json",'r') as f:
            _weapons = json.load(f)
    return _weapons

def getArmor():
    global _armor
    if _armor == None:
        with open("data\\armor.json",'r') as f:
            _armor = json.load(f)
    return _armor

def getAccessories():
    global _accessories
    if _accessories == None:
        with open("data\\accessories.json",'r') as f:
            _accessories = json.load(f)
    return _accessories

def getAmmo():
    global _ammo
    if _ammo == None:
        with open("data\\ammo.json",'r') as f:
            _ammo = json.load(f)
    return _ammo

def getBait():
    global _bait
    if _bait == None:
        with open("data\\bait.json",'r') as f:
            _bait = json.load(f)
    return _bait

def getCrafting():
    global _crafting
    if _crafting == None:
        with open("data\\crafting.json",'r') as f:
            _crafting = json.load(f)
    return _crafting

def getBrewing():
    global _brewing
    if _brewing == None:
        with open("data\\brewing.json",'r') as f:
            _brewing = json.load(f)
    return _brewing

def getBanned():
    global _banned
    if _banned == None:
        with open("data\\banned.json",'r') as f:
            _banned = json.load(f)
    return _banned

def getOres():
    global _ores
    if _ores == None:
        with open("data\\ores.json",'r') as f:
            _ores = json.load(f)
    return _ores

def getMobs():
    global _mobs
    if _mobs == None:
        with open("data\\mobs.json",'r') as f:
            _mobs = json.load(f)
    return _mobs

def getResources():
    global _resources
    if _resources == None:
        with open("data\\resources.json",'r') as f:
            _resources = json.load(f)
    return _resources

def getMap():
    global _map
    if _map == None:
        with io.open("data\\map.json",mode='r',encoding="utf-16") as f:
            _map = json.load(f)
    return _map





### WRITES ###

def writeUsers():
    global _users
    getUsers()
    with open("data\\users.json",'w') as f:
        json.dump(_users,f,indent=4,sort_keys=True)

def writeItems():
    global _items
    getItems()
    with open("data\\items.json",'w') as f:
        json.dump(_items,f,indent=4,sort_keys=True)

def writeItemsOg():
    global _itemsog
    getItemsOg()
    with open("data\\itemsog.json",'w') as f:
        json.dump(_itemsog,f,indent=4,sort_keys=True)

def writeFoods():
    global _foods
    getFoods()
    with open("data\\foods.json",'w') as f:
        json.dump(_foods,f,indent=4,sort_keys=True)

def writePickaxes():
    global _pickaxes
    getPickaxes()
    with open("data\\pickaxes.json",'w') as f:
        json.dump(_pickaxes,f,indent=4,sort_keys=True)

def writeRods():
    global _rods
    getRods()
    with open("data\\rods.json",'w') as f:
        json.dump(_rods,f,indent=4,sort_keys=True)

def writeWeapons():
    global _weapons
    getWeapons()
    with open("data\\weapons.json",'w') as f:
        json.dump(_weapons,f,indent=4,sort_keys=True)

def writeArmor():
    global _armor
    getArmor()
    with open("data\\armor.json",'w') as f:
        json.dump(_armor,f,indent=4,sort_keys=True)

def writeAccessories():
    global _accessories
    getAccessories()
    with open("data\\accessories.json",'w') as f:
        json.dump(_accessories,f,indent=4,sort_keys=True)

def writeAmmo():
    global _ammo
    getAmmo()
    with open("data\\ammo.json",'w') as f:
        json.dump(_ammo,f,indent=4,sort_keys=True)

def writeBait():
    global _bait
    getBait()
    with open("data\\bait.json",'w') as f:
        json.dump(_bait,f,indent=4,sort_keys=True)

def writeCrafting():
    global _crafting
    getCrafting()
    with open("data\\crafting.json",'w') as f:
        json.dump(_crafting,f,indent=4,sort_keys=True)

def writeBrewing():
    global _brewing
    getBrewing()
    with open("data\\brewing.json",'w') as f:
        json.dump(_brewing,f,indent=4,sort_keys=True)

def writeBanned():
    global _banned
    getBanned()
    with open("data\\banned.json",'w') as f:
        json.dump(_banned,f,indent=4,sort_keys=True)

def writeOres():
    global _ores
    getOres()
    with open("data\\ores.json",'w') as f:
        json.dump(_ores,f,indent=4,sort_keys=True)

def writeMobs():
    global _mobs
    getMobs()
    with open("data\\mobs.json",'w') as f:
        json.dump(_mobs,f,indent=4,sort_keys=True)

def writeResources():
    global _resources
    getResources()
    with open("data\\resources.json",'w') as f:
        json.dump(_resources,f,indent=4,sort_keys=True)

def writeMap():
    global _map
    getMap()
    with io.open("data\\map.json",mode='w',encoding="utf-16") as f:
        json.dump(_map,f,indent=4,sort_keys=True)
