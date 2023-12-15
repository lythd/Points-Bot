from scipy.stats import binom
import numpy as np
import random
import time

def v(item):
    match item:
        case "orechunk":
            return 0
        case "coal":
            return 1
        case "copperore":
            return 10
        case "tinore":
            return 20
        case "ironore":
            return 30
        case "silverore":
            return 40
        case "goldore":
            return 50
        case "diamond":
            return 60
        case "emerald":
            return 60
    return -1

def method1(t,i,r,p=False):
    c = 0
    n = v(i)
    for _ in range(t):
        tc = random.randrange(-n,3)
        if tc < 0:
            tc = 0
        if r and tc == 2:
            tc = 1
        c += tc
    if p: print("You found {} of {} after mining {} times!".format(c,i,t))

def binomial(n,p):
    x = np.arange(0, n+1)
    weights = binom.pmf(x, n, p)
    res = random.choices(x,weights=weights)[0]
    return res

def method2(t,i,r,p=False):
    n = v(i)
    n0 = binomial(t,(n+1)/(n+3))
    c = t-n0
    if not r:
        c += binomial(c,0.5)
    if p: print("You found {} of {} after mining {} times!".format(c,i,t))

def testthem(n,t,i,r,p):
    t1 = time.process_time_ns()
    for _ in range(n):
        method1(t,i,r,p)
    t2 = time.process_time_ns()
    print("Method1 took {} ms on avg for {} times.".format(((t2-t1)/1000000)/n,t))
    t1 = time.process_time_ns()
    for _ in range(n):
        method2(t,i,r,p)
    t2 = time.process_time_ns()
    print("Method2 took {} ms on avg for {} times.".format(((t2-t1)/1000000)/n,t))


def mainloop():
    trues = ["t","true","y","yes"]
    falses = ["f","false","n","no"]
    while True:
        n = ""
        while isinstance(n,str):
            try:
                n = int(n)
            except:
                n = input("How many tests: ")
        t = ""
        while isinstance(t,str):
            try:
                t = int(t)
            except:
                t = input("How many times/test: ")
        i = ""
        while v(i) < 0:
            i = input("What item: ")
        r = ""
        while isinstance(r,str):
            r = input("Reduced: ").lower()
            if r in trues:
                r = True
            elif r in falses:
                r = False
        p = ""
        while isinstance(p,str):
            p = input("Print: ").lower()
            if p in trues:
                p = True
            elif p in falses:
                p = False
        testthem(n,t,i,r,p)

mainloop()
    