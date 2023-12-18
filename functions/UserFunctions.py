
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













#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### USERS ###
    
def beg_this(user):
    users = getUsers()
    try:
        if str(date.today()) == users[str(user.id)]["lastbeg"]:
            return -1
    except:
        pass
    earnings = random.randrange(101)
    users[str(user.id)]["money"] += earnings
    users[str(user.id)]["lastbeg"] = str(date.today())
    writeUsers()
    return earnings

def open_account(user):
    users = getUsers()
        
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)]= {}
        users[str(user.id)]["name"] = user.name
        users[str(user.id)]["quests"] = 0
        users[str(user.id)]["money"] = 200
        users[str(user.id)]["energy"] = 100
        users[str(user.id)]["location"] = "skycity"
        users[str(user.id)]["gang"] = "None"
        users[str(user.id)]["pumpkinseed"] = False
        users[str(user.id)]["rocketacquired"] = False
        users[str(user.id)]["processes"] = []
        users[str(user.id)]["factories"] = {}
        users[str(user.id)]["equipment"] = ["None","None","None","None"]
        
    writeUsers()
    return True

def update_bank(user,change = 0):
    users = getUsers()
    
    users[str(user.id)]["name"] = user.name
    users[str(user.id)]["money"] += change
    
    writeUsers()
        
    bal = users[str(user.id)]["money"]
    return bal

def update_bank_by_id(id,change = 0):
    users = getUsers()
    
    users[str(id)]["money"] += change
    
    writeUsers()
        
    bal = users[str(id)]["money"]
    return bal

def update_energy(user,change = 0):
    users = getUsers()
    
    users[str(user.id)]["name"] = user.name
    users[str(user.id)]["energy"] += change
    
    writeUsers()
        
    energy = users[str(user.id)]["energy"]
    return energy