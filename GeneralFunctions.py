
#---------------------------------------------------------------------------SETUP----------------------------------------------------------------------------------------#

### IMPORTS ###

## DISCORD ##
import discord
from discord.ext import commands
from discord import app_commands
from discord import Color
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
















#---------------------------------------------------------------------------FUNCTIONS----------------------------------------------------------------------------------------#

### STRINGS ###

def format_number(number):
    num_str = str(number)
    if len(num_str) <= 3:
        return num_str
    pos = len(num_str) % 3
    formatted_num = num_str[:pos]
    while pos < len(num_str):
        if pos > 0: formatted_num += ","
        formatted_num += num_str[pos:pos+3]
        pos += 3
    return formatted_num

def format(str):
    newstr = ""
    for c in str:
        if not c in " '":
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







## COLORS ##

def colorGood():
    return Color.green()
def colorBad():
    return Color.orange()
def colorError():
    return Color.red()
def colorMap():
    return Color.teal()
def colorTransaction():
    return Color.gold()
def colorShop():
    return Color.yellow()
def colorInfo():
    return Color.blurple()
def colorLeaderboard():
    return Color(0xfa43ee)
def colorEquipment():
    return Color.dark_blue()
def colorMining():
    return Color.dark_gray()
def colorCrafting():
    return Color.dark_orange()
def colorFishing():
    return Color.blue()
def colorFighting():
    return Color.dark_red()
def colorQuest():
    return Color.magenta()
def colorPlot():
    return Color.greyple()
def colorFactory():
    return Color.light_gray()
def colorGang():
    return Color.purple()
def colorElection():
    return Color.from_rgb(255,255,255)
def colorWar():
    return Color.dark_red()








### MISC ###

def curTime():
    return round(time.time() * 1000)