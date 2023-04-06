# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 13:46:46 2023

@author: pwint
"""
import copy as c
import numpy as np
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
    
def ptohit_l(off,_def): # chance to hit with melee weapon with lightning reflexes
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
avgdmg_me_lr=lambda off,_str,ap,_def,res,arm: ptohit_l(off,_def)*ptowound(_str,res)*n_ptoarm(ap,arm)
avgdmg_autohits=lambda n,_str,ap,_def,res,arm:n*ptowound(_str, res)*n_ptoarm(ap,arm)
avgdmg_mi=lambda aim,_str,ap,res,arm: paim(aim)*ptowound(_str, res)*n_ptoarm(ap, arm)
avgdmgpt=lambda dmg,pt: dmg/pt

def missile(att,aim,_str,ap,pt,test=False):
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

# todo: multiple wound, auto hits
# treat breath as an additional modelpart with auto hits
def single_melee(att,off,_str,ap,pt,lr=False,autohits=0,mw=1,test=False):
    if test==True:
        l1=[["def","res","arm","dmg","norm"]]
    l2=[]
    for _def in range(2,8):
        for res in range(2,7):
            for arm in range(0,7):
                if lr==False:
                    dmg=att*mw*avgdmg_me(off,_str,ap,_def,res,arm)+avgdmg_autohits(autohits, _str, ap, _def, res, arm)
                else:
                    dmg=att*mw*avgdmg_me_lr(off,_str,ap,_def,res,arm)+avgdmg_autohits(autohits, _str, ap, _def, res, arm)
                dmgpt=avgdmgpt(100*dmg,pt)
                if test==True:
                    l1.append([_def,res,arm,round(dmg,1),round(dmgpt,1)])
                l2.append([_def,res,arm,round(dmg,1),round(dmgpt,1)])
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

def multi_melee(att,off,_str,ap,pt,lr,autohits,mw,test=False):
    if test==True:
        l1=[["def","res","arm","dmg","norm"]]
    l2=[]
    for _def in range(2,8):
        for res in range(2,7):
            for arm in range(0,7):
                dmg=0
                dmgpt=0
                for i in range(len(att)):
                    if lr[i]==False:
                        dmg+=att[i]*mw[i]*avgdmg_me(off[i],_str[i],ap[i],_def,res,arm)+avgdmg_autohits(autohits[i], _str[i], ap[i], _def, res, arm)
                    else:
                        dmg+=att[i]*mw[i]*avgdmg_me_lr(off[i],_str[i],ap[i],_def,res,arm)+avgdmg_autohits(autohits[i], _str[i], ap[i], _def, res, arm)
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

def melee(att,off,_str,ap,pt,lr,autohits,mw,test=False):
    if type(att)==list:
        return multi_melee(att, off, _str, ap, pt, lr,autohits,mw,test)
    else:
        return single_melee(att, off, _str, ap, pt,lr,autohits,mw,test)
    
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
    a1=np.array(l1)[:,3:] # get dmg and norm from l1
    a2=np.array(l2)[:,3:] # get dmg and norm from l2
    if (a2>0).all:
        a3=(a1/a2).round(1).copy() # calculates relative dmg/norm
        a3=np.concatenate((np.array(l1)[:,:3],a3),1)
        lret = a3.tolist()
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
        
tofile=lambda fname,l: np.savetxt(fname,np.array(l))
loadfile=lambda fname: np.loadtxt(fname).tolist()
    