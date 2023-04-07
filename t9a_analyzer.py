# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 13:46:46 2023

@author: pwint
"""
import copy as c
import numpy as np
import pathlib as pl
#import pprint as pp

def ptohit(off,_def): # chance to hit with melee weapon
    if off-_def>=4:
        return 5/6
    elif off-_def>=1:
        return 4/6
    elif off-_def>=-3:
        return 3/6
    elif off-_def>=-7:
        return 2/6
    else:
        return 1/6
    
def ptohit_lr(off,_def): # chance to hit with melee weapon with lightning reflexes
    if off-_def>=4:
        return 5/6
    elif off-_def>=1:
        return 5/6
    elif off-_def>=-3:
        return 4/6
    elif off-_def>=-7:
        return 3/6
    else:
        return 2/6

def paim(aim): # chance to hit with missile weapon
    if aim>8:
        return 0/6
    elif aim>=7:
        return 1/12
    else:
        return min((7-aim)/6,5/6)

def ptowound(_str,res): # chance to wound
    if _str-res>=2:
        return 5/6
    elif _str-res>=1:
        return 4/6
    elif _str-res>=0:
        return 3/6
    elif _str-res>=-1:
        return 2/6
    else:
        return 1/6
    
def n_ptoarm(ap,arm): # chance to fail armour save
    if ap>arm:
        return 6/6
    else:
        return max(1-(arm-ap)/6,1/6)
    
avgdmg_me=lambda off,_str,ap,_def,res,arm: ptohit(off,_def)*ptowound(_str,res)*n_ptoarm(ap,arm)
avgdmg_me_lr=lambda off,_str,ap,_def,res,arm: ptohit_lr(off,_def)*ptowound(_str,res)*n_ptoarm(ap,arm)
avgdmg_autohits=lambda n,_str,ap,_def,res,arm:n*ptowound(_str, res)*n_ptoarm(ap,arm)
avgdmg_mi=lambda aim,_str,ap,res,arm: paim(aim)*ptowound(_str, res)*n_ptoarm(ap, arm)
avgdmgpt=lambda dmg,pt: dmg/pt

def missile(att,aim,_str,ap,pt,acc=False,qtf=False,unw=False,sta=False,test=False):
    if test==True:
        l1=[["res","arm","dmg","norm"]]
    l2=[]
    for res in range(2,7):
        for arm in range(0,7):
            dmg=att*avgdmg_mi(aim, _str, ap, res, arm)
            dmgpt=avgdmgpt(100*dmg,pt)
            if test==True:
                l1.append([res,arm,round(dmg,1),round(dmgpt,1)])
            l2.append([res,arm,round(dmg,1),round(dmgpt,1)])
        if test==True:
            l1.append(['','','','',''])
    if test==True:
        for row in l1:
            print("{: >5} {: >5} {: >5} {: >5}".format(*row))
    if test==False:
        return l2

# treat breath as an additional modelpart with 0 attack and auto hits
def melee(att,off,_str,ap,pt,mw,autohits,lr,test=False):
    if test==True:
        l1=[["def","res","arm","dmg","norm"]]
    l2=[]
    for _def in range(2,8):
        for res in range(2,7):
            for arm in range(0,7):
                dmg=0
                dmgpt=0
                if type(att)==list:
                    for i in range(len(att)):
                        if lr[i]==False:
                            dmg+=att[i]*mw[i]*avgdmg_me(off[i],_str[i],ap[i],_def,res,arm)+avgdmg_autohits(autohits[i], _str[i], ap[i], _def, res, arm)
                        else:
                            dmg+=att[i]*mw[i]*avgdmg_me_lr(off[i],_str[i],ap[i],_def,res,arm)+avgdmg_autohits(autohits[i], _str[i], ap[i], _def, res, arm)
                else:
                    if lr==False:
                        dmg=att*mw*avgdmg_me(off,_str,ap,_def,res,arm)+avgdmg_autohits(autohits, _str, ap, _def, res, arm)
                    else:
                        dmg=att*mw*avgdmg_me_lr(off,_str,ap,_def,res,arm)+avgdmg_autohits(autohits, _str, ap, _def, res, arm)
                dmgpt+=avgdmgpt(100*dmg,pt)
                if test==True:
                    l1.append([_def,res,arm,round(dmg,1),round(dmgpt,1)])
                l2.append([_def,res,arm,round(dmg,1),round(dmgpt,1)])
                dmg=0
                dmgpt=0
            if test==True:
                l1.append(['','','','',''])
        if test==True:
            pass #l1.append(2*['','','','',''])
    if test==True:
        ltest=c.copy([6*l1[0]])
        for i in range(40):
            # ltest.append(l1[0+1]+l1[35+1]+...)
            # ltest.append(l1[1+1]+l1[36+1]+...)
            #...
            # ltest.append(l1[34+1]+l1[69+1]...)
            ltemp=[]
            for j in range(6):
                ltemp+=c.copy(l1[i+40*j+1])
            ltest.append(ltemp)
        for row in ltest:
            print("{: >7} {: >3} {: >3} {: >5} {: >5} {: >7} {: >3} {: >3} {: >5} {: >5}{: >7} {: >3} {: >3} {: >5} {: >5}{: >7} {: >3} {: >3} {: >5} {: >5}{: >7} {: >3} {: >3} {: >5} {: >5}{: >7} {: >3} {: >3} {: >5} {: >5}".format(*row))
    if test==False:
        return l2
    
def melee_filter(att,off,_str,ap,pt,lr,autohits,mw,_def=-1,res=-1,arm=-1,test=False):
    l=melee(att,off,_str,ap,pt,lr,autohits,mw)
    lret=[]
    if test==True:
        ltest=[["def","res","arm","dmg","norm"]]
    if _def!=-1:
        for i in range(len(l)):
            if l[i][0]==_def:
                lret.append(l[i])
                if test==True:
                    ltest.append(l[i])
        l=lret
    if res!=-1:
        lret=[]
        ltest=[["def","res","arm","dmg","norm"]]
        for i in range(len(l)):
            if l[i][1]==res:
                lret.append(l[i])
                if test==True:
                    ltest.append(l[i])
        l=lret
    if arm!=-1:
        lret=[]
        ltest=[["def","res","arm","dmg","norm"]]
        for i in range(len(l)):
            if l[i][2]==arm:
                lret.append(l[i])
                if test==True:
                    ltest.append(l[i])
    if test==True:
        for row in ltest:
            print("{: >5} {: >5} {: >5} {: >5} {: >5}".format(*row))
    if test==False:
        return lret
    
def melee_compare(l1,l2,test=False):
    arra=np.array(l1)[:,3:] # get dmg and norm from l1
    arrb=np.array(l2)[:,3:] # get dmg and norm from l2
    if (arrb>0).all:
        arrc=(arra/arrb).round(1).copy() # calculates relative dmg/norm
        arrc=np.concatenate((np.array(l1)[:,:3],arrc),1)
        lret = arrc.tolist()
        if test==True:
            ltest=c.copy([6*["def","res","arm","dmg","norm"]])
            for i in range(35):
                # ltest.append(l1[0+1]+l1[35+1]+...)
                # ltest.append(l1[1+1]+l1[36+1]+...)
                #...
                # ltest.append(l1[34+1]+l1[69+1]...)
                ltemp=[]
                if i%7 == 0 and i!=0:
                    ltest.append(6*['','','','',''])
                for j in range(6):
                    ltemp+=c.copy(lret[i+35*j])
                ltest.append(ltemp)
            for row in ltest:
                print("{: >7} {: >4} {: >4} {: >4} {: >4} {: >7} {: >4} {: >4} {: >4} {: >4} {: >7} {: >4} {: >4} {: >4} {: >4} {: >7} {: >4} {: >4} {: >4} {: >4} {: >7} {: >4} {: >4} {: >4} {: >4} {: >7} {: >4} {: >4} {: >4} {: >4}".format(*row))
        if test==False:
            return lret
        
wf=lambda fname,l: np.savetxt("./data/"+fname+".txt",np.array(l))
lf=lambda fname: np.loadtxt("./data/"+fname+".txt").tolist()

def wr_he():
    # Core
    # Citizen Spears
    wf("cs_chd",melee(20, 4, 3, 2, 260, 1, 0, True))
    wf("cs",melee(20, 4, 3, 1, 260, 1, 0, True))
    # Highborn Lancers
    wf("hl_chg",melee([5,5], [4,3], [5,3], [2,0], 210, [1,1], [0,0], [True,False]))
    wf("hl",melee([5,5], [4,3], [3,3], [0,0], 210, [1,1], [0,0], [True,False]))
    # Ellein Reavers
    wf("er_me_chg",melee([5,5], [4,3], [4,3], [1,0], 180, [1,1], [0,0], [True,False]))
    wf("er_me",melee([5,5], [4,3], [3,3], [0,0], 180, [1,1], [0,0], [True,False]))
    wf("er_mi",missile(5,3,3,0,180))
    # Citizen Archers
    wf("ca_me",melee(10, 4, 3, 0, 150, 1, 0, True))
    wf("ca_mi",missile(10, 3, 3, 0, 150))
    # Seaguard
    wf("sg_me_chd",melee(15, 4, 3, 2, 240, 1, 0, True))
    wf("sg_me",melee(15, 4, 3, 1, 240, 1, 0, True))
    wf("sg_mi",missile(15, 3, 3, 0, 240))
    
    # Special
    # Sword Masters
    wf("sm",melee(10,6,5,2,125,1,0,True))
    # Lion Guard
    wf("lg_mw",melee(10, 5, 6, 3, 220, 2, 0, False))
    wf("lg",melee(10, 5, 6, 3, 220, 1, 0, False))
    # Flame Wardens
    wf("fw",melee(15, 5, 4, 1, 260, 1, 0, True))
    # Knights of Ryma
    wf("kor_chg",melee([10,5], [5,3], [6,3], [3,0], 320, [1,1], [0,0], [True,False]))
    wf("kor",melee([10,5], [5,3], [4,3], [1,0], 320, [1,1], [0,0], [True,False]))
    # Reaver Chariots
    wf("rc_me_chg",melee([2,2,0], [4,3,0], [4,3,5], [1,0,2], 90, [1,1,1], [0,0,3.5], [True,False,False]))
    wf("rc_me",melee([2,2,0], [4,3,0], [3,3,5], [0,0,2], 90, [1,1,1], [0,0,0], [True,False,False]))
    wf("rc_mi",missile(2, 3, 3, 0, 90))
    # Lion Chariot
    wf("lc_chg_mw",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195, [2,1,1], [0,0,4.5], [False,False,False]))
    wf("lc_chg",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195, [1,1,1], [0,0,4.5], [False,False,False]))
    wf("lc_mw",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195, [2,1,1], [0,0,0], [False,False,False]))
    wf("lc",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195, [1,1,1], [0,0,0], [False,False,False]))
    # Giant Eagles
    wf("ge_st",melee(2, 5, 4, 1, 100, 1, 1, False)) # Large => stomp(1)
    wf("ge",melee(2, 5, 4, 1, 100, 1, 0, False))
    # Frost Phoenix
    wf("frp_st",melee(4, 5+2, 5, 2, 340, 1, 3.5, False)) # Gigantic => stomp(d6)
    wf("frp_wb_st",melee([4,2], [5+2,5+2], [5,4], [2,1], 380, [1,1], [3.5,0], [False,True])) # Gigantic => stomp(d6)
    wf("frp",melee(4, 5+2, 5, 2, 340, 1, 0, False))
    wf("frp_wb",melee([4,2], [5+2,5+2], [5,4], [2,1], 380, [1,1], [0,0], [False,True]))
    #Fire Phoenix
    wf("fip_st",melee([4,0], [5,0], [5,4], [2,1], 365, [1,1], [3.5,3.5], [False,False])) # Gigantic => stomp(d6)
    wf("fip_wb_st",melee([4,0,2], [5,0,5], [5,4,4], [2,1,1], 365, [1,1,1], [3.5,3.5,0], [False,False,False])) # Gigantic => stomp(d6)
    wf("fip",melee([4,0], [5,0], [5,4], [2,1], 365, [1,1], [0,3.5], [False,False]))
    wf("fip_wb",melee([4,0,2], [5,0,5], [5,4,4], [2,1,1], 365, [1,1,1], [0,3.5,0], [False,False,False]))
    # Initiate of the Fiercy Heart
    wf("iotfh_st_br",melee([1,4,0], [4,5,0], [3,5,4], [0,2,1], 330, [1,1,1], [0,1,7], [True,False,False])) # Large => stomp(1)
    wf("iotfh_br",melee([1,4,0], [4,5,0], [3,5,4], [0,2,1], 330, [1,1,1], [0,0,7], [True,False,False]))
    wf("iotfh_st",melee([1,4], [4,5], [3,5], [0,2], 330, [1,1], [0,1], [True,False])) # Large => stomp(1)
    wf("iotfh",melee([1,4], [4,5], [3,5], [0,2], 330, [1,1], [0,0], [True,False]))
    
    
