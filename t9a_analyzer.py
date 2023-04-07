# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 13:46:46 2023

@author: pwint
"""
import copy as c
import numpy as np
#import pathlib as pl
#import pprint as pp

def ptohit(off,_def,mod=0): # chance to hit with melee weapon
    if off-_def>=4:
        p=(5+mod)/6
    elif off-_def>=1:
        p=(4+mod)/6
    elif off-_def>=-3:
        p=(3+mod)/6
    elif off-_def>=-7:
        p=(2+mod)/6
    else:
        p=(1+mod)/6
    if p>5/6:
        return 5/6
    elif p>=1/6:
        return p
    else:
        return 1/6

def paim(aim): # chance to hit with missile weapon
    if aim>8:
        return 0/6
    elif aim>=7:
        return 1/12
    else:
        return min((7-aim)/6,5/6)

def ptowound(_str,res,mod=0): # chance to wound
    if _str-res>=2:
        p=(5+mod)/6
    elif _str-res>=1:
        p=(4+mod)/6
    elif _str-res>=0:
        p=(3+mod)/6
    elif _str-res>=-1:
        p=(2+mod)/6
    else:
        p=(1+mod)/6
    if p>5/6:
        return 5/6
    elif p>=1/6:
        return p
    else:
        return 1/6
    
def n_ptoarm(ap,arm): # chance to fail armour save
    if ap>arm:
        return 6/6
    else:
        return max(1-(arm-ap)/6,1/6)
    
avgdmg_me=lambda off,_str,ap,_def,res,arm,hmod=0,wmod=0: ptohit(off,_def,hmod)*ptowound(_str,res,wmod)*n_ptoarm(ap,arm)
avgdmg_autohits=lambda n,_str,ap,res,arm,wmod=0:n*ptowound(_str, res,wmod)*n_ptoarm(ap,arm)
avgdmg_mi=lambda aim,_str,ap,res,arm,wmod=0: paim(aim)*ptowound(_str, res,wmod)*n_ptoarm(ap, arm)
avgdmgpt=lambda dmg,pt: dmg/pt

def show(l1):
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
            ltemp+=c.copy(l1[i+35*j])
        ltest.append(ltemp)
    for row in ltest:
        print("{: >7} {: >4} {: >4} {: >4} {: >4} {: >7} {: >4} {: >4} {: >4} {: >4} {: >7} {: >4} {: >4} {: >4} {: >4} {: >7} {: >4} {: >4} {: >4} {: >4} {: >7} {: >4} {: >4} {: >4} {: >4} {: >7} {: >4} {: >4} {: >4} {: >4}".format(*row))

def missile(att,aim,_str,ap,pt,mw=1,aa=1,acc=False,qtf=False,unw=False,mof=False,sta=False,rel=False,test=False):
    if test==True:
        l1=[["aim","res","arm","dmg","norm"]]
    l2=[]
    aim_orig=aim
    if type(att)==list: # extend optional parameters to lists
        if type(mw)!=list:
            mw=[mw for i in range(len(att))]
        if type(aa)!=list:
            aa=[aa for i in range(len(att))]
    for sit in range(6):
        aim=aim_orig
        # 0 => Short Range, no mod.
        # Long Range
        if sit==1 and acc==False:
            aim+=1
        # Move and Shoot
        elif sit==2 and mof==True: # Move or Fire
            aim=90
        elif sit==2 and ((qtf==False and unw==False) or (qtf==True and unw==True)): # qick to fire = unwieldy
            aim+=1
        elif sit==2 and (qtf==False and unw==True): # unwieldy
            aim+=2 
        # Stand and Shoot
        elif sit==3 and rel==True: # Reload!
            aim=90
        elif sit==3 and sta==False:
            aim+=1
            # Soft Cover
        elif sit==4:
            aim+=1
        # Hard Cover
        elif sit==5:
            aim+=2
        for res in range(2,7):
            for arm in range(0,7):
                dmg=0
                if type(att)==list:
                    for i in range(len(att)):
                        dmg+=att[i]*mw[i]*aa[i]*avgdmg_mi(aim, _str[i], ap[i], res, arm)
                else:
                    dmg+=att*mw*aa*avgdmg_mi(aim, _str, ap, res, arm)
                dmgpt=avgdmgpt(100*dmg,pt)
                if test==True:
                    l1.append([aim,res,arm,round(dmg,1),round(dmgpt,1)])
                l2.append([aim,res,arm,round(dmg,1),round(dmgpt,1)])
            if test==True:
                l1.append(['','','','','',''])
    if test==True:
        ltest=[['','','Short','Range','']+['','','Long','Range','']+['','Move','and','Shoot','']+['','Stand','and','Shoot','']+['','','Soft','Cover','']+['','','Hard','Cover','']]
        ltest.append(6*["aim","res","arm","dmg","norm"])
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
            print("{: >7} {: >5} {: >5} {: >5} {: >5} {: >7} {: >5} {: >5} {: >5} {: >5} {: >7} {: >5} {: >5} {: >5} {: >5} {: >7} {: >5} {: >5} {: >5} {: >5} {: >7} {: >5} {: >5} {: >5} {: >5} {: >7} {: >5} {: >5} {: >5} {: >5}".format(*row))
    if test==False:
        return l2

# treat breath as an additional modelpart with 0 attack and auto hits
def melee(att,off,_str,ap,pt,mw=1,autohits=0,hmod=0,wmod=0,test=False):
    if test==True:
        l1=[["def","res","arm","dmg","norm"]]
    l2=[]
    if type(att)==list: # extend optional parameters to lists
        if type(mw)!=list:
            mw=[mw for i in range(len(att))]
        if type(autohits)!=list:
            autohits=[autohits for i in range(len(att))]
        if type(hmod)!=list:
            hmod=[hmod for i in range(len(att))]
        if type(wmod)!=list:
            wmod=[wmod for i in range(len(att))]
    for _def in range(2,8):
        for res in range(2,7):
            for arm in range(0,7):
                dmg=0
                if type(att)==list:
                    for i in range(len(att)):
                        dmg+=att[i]*mw[i]*avgdmg_me(off[i],_str[i],ap[i],_def,res,arm,hmod[i],wmod[i])+avgdmg_autohits(autohits[i], _str[i], ap[i], res, arm,wmod=wmod[i])
                else:
                    dmg=att*mw*avgdmg_me(off,_str,ap,_def,res,arm,hmod,wmod)+avgdmg_autohits(autohits, _str, ap, res, arm,wmod)
                dmgpt=avgdmgpt(100*dmg,pt)
                if test==True:
                    l1.append([_def,res,arm,round(dmg,1),round(dmgpt,1)])
                l2.append([_def,res,arm,round(dmg,1),round(dmgpt,1)])
            if test==True:
                l1.append(['','','','',''])
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
            print("{: >7} {: >3} {: >3} {: >5} {: >5} {: >7} {: >3} {: >3} {: >5} {: >5} {: >7} {: >3} {: >3} {: >5} {: >5} {: >7} {: >3} {: >3} {: >5} {: >5} {: >7} {: >3} {: >3} {: >5} {: >5} {: >7} {: >3} {: >3} {: >5} {: >5}".format(*row))
    if test==False:
        return l2
    
def melee_filter(att,off,_str,ap,pt,mw=1,autohits=0,hmod=0,wmod=0,_def=-1,res=-1,arm=-1,test=False):
    l=melee(att,off,_str,ap,pt,mw,autohits,hmod,wmod)
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
    # Characters
    
    # Mounts
    
    # Core
    # Citizen Spears
    wf("cs_chd",melee(20, 4, 3, 2, 260, hmod=1))
    wf("cs",melee(20, 4, 3, 1, 260, hmod=1))
    # Highborn Lancers
    wf("hl_chg",melee([5,5], [4,3], [5,3], [2,0], 210, hmod=[1,0]))
    wf("hl",melee([5,5], [4,3], [3,3], [0,0], 210, hmod=[1,0]))
    # Ellein Reavers
    wf("er_me_chg",melee([5,5], [4,3], [4,3], [1,0], 180, hmod=[1,0]))
    wf("er_me",melee([5,5], [4,3], [3,3], [0,0], 180, hmod=[1,0]))
    wf("er_mi",missile(5,3,3,0,180))
    # Citizen Archers
    wf("ca_me",melee(10, 4, 3, 0, 150, hmod=1))
    wf("ca_mi",missile(10, 3, 3, 0, 150,acc=True))
    # Seaguard
    wf("sg_me_chd",melee(15, 4, 3, 2, 240, hmod=1))
    wf("sg_me",melee(15, 4, 3, 1, 240, hmod=1))
    wf("sg_mi",missile(15, 3, 3, 0, 240,sta=True))
    
    # Special
    # Sword Masters
    wf("sm",melee(10,6,5,2,125,hmod=1))
    # Lion Guard
    wf("lg_mw",melee(10, 5, 6, 3, 220, mw=2))
    wf("lg",melee(10, 5, 6, 3, 220))
    # Flame Wardens
    wf("fw",melee(15, 5, 4, 1, 260, hmod=1))
    # Knights of Ryma
    wf("kor_chg",melee([10,5], [5,3], [6,3], [3,0], 320, hmod=[1,0]))
    wf("kor",melee([10,5], [5,3], [4,3], [1,0], 320, hmod=[1,0]))
    # Reaver Chariots
    wf("rc_me_chg",melee([2,2,0], [4,3,0], [4,3,5], [1,0,2], 90, autohits=[0,0,3.5], hmod=[1,0,0]))
    wf("rc_me",melee([2,2,0], [4,3,0], [3,3,5], [0,0,2], 90, hmod=[1,0,0]))
    wf("rc_mi",missile(2, 3, 3, 0, 90))
    # Lion Chariot
    wf("lc_chg_mw",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195, mw=[2,1,1], autohits=[0,0,4.5]))
    wf("lc_chg",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195, autohits=[0,0,4.5]))
    wf("lc_mw",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195, mw=[2,1,1]))
    wf("lc",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195))
    # Giant Eagles
    wf("ge_st",melee(2, 5, 4, 1, 100)) # Large => stomp(1)
    wf("ge",melee(2, 5, 4, 1, 100))
    # Frost Phoenix
    wf("frp_st",melee(4, 5+2, 5, 2, 340, autohits=3.5)) # Gigantic => stomp(d6)
    wf("frp_wb_st",melee([4,2], [5+2,5+2], [5,4], [2,1], 380, autohits=[3.5,0], hmod=[0,1])) # Gigantic => stomp(d6)
    wf("frp",melee(4, 5+2, 5, 2, 340))
    wf("frp_wb",melee([4,2], [5+2,5+2], [5,4], [2,1], 380, hmod=[0,1]))
    #Fire Phoenix
    wf("fip_st",melee([4,0], [5,0], [5,4], [2,1], 365, autohits=[3.5,3.5])) # Gigantic => stomp(d6)
    wf("fip_wb_st",melee([4,0,2], [5,0,5], [5,4,4], [2,1,1], 365, autohits=[3.5,3.5,0], hmod=[0,0,1])) # Gigantic => stomp(d6)
    wf("fip",melee([4,0], [5,0], [5,4], [2,1], 365, autohits=[0,3.5]))
    wf("fip_wb",melee([4,0,2], [5,0,5], [5,4,4], [2,1,1], 365, autohits=[0,3.5,0], hmod=[0,0,1]))
    # Initiate of the Fiercy Heart
    wf("iotfh_st_br",melee([1,4,0], [4,5,0], [3,5,4], [0,2,1], 330, autohits=[0,1,7], hmod=[1,0,0])) # Large => stomp(1)
    wf("iotfh_br",melee([1,4,0], [4,5,0], [3,5,4], [0,2,1], 330, autohits=[0,0,7], hmod=[1,0,0]))
    wf("iotfh_st",melee([1,4], [4,5], [3,5], [0,2], 330, [1,1], autohits=[0,1], hmod=[1,0])) # Large => stomp(1)
    wf("iotfh",melee([1,4], [4,5], [3,5], [0,2], 330, hmod=[1,0]))
    # Sea Guard Reaper
    wf("sgr_me",melee(2, 4, 3, 0, 190,hmod=1))
    wf("sgr_mi_1_1",missile(1, 3, 6, 10, 180,mw=2,mof=True,rel=True))
    wf("sgr_mi_1_5",missile([1,1], 3, [3,6], [10,10], 180,mw=[1,2],aa=[4,1],mof=True,rel=True))
    wf("sgr_mi_6",missile(6, 3, 4, 2, 180,mof=True,rel=True))
    # Sky Sloop
    wf("ss_me_chg",melee([2,2,0],[4,4,0],[4,4,5],[1,1,2],225,autohits=[0,0,3.5],hmod=[1,0,0]))
    wf("ss_me",melee([2,2,0],[4,4,0],[3,4,5],[0,1,2],225,autohits=[0,0,0],hmod=[1,0,0]))
    wf("ss_mi",missile(4,3,5,3,225,qtf=True,rel=True))
    
    # Queen's Bows
    # Queen's Guard
    wf("qg_me",melee(5, 5, 3, 0, 135,hmod=1))
    wf("qg_me_s_chd",melee(5, 5, 3, 2, 140,hmod=1))
    wf("qg_me_s",melee(5, 5, 3, 1, 140,hmod=1))
    wf("qg_mi",missile(5, 2, 4, 1, 135))
    # Grey Watchers
    wf("gw_me",melee(5, 4, 3, 0, 135))
    wf("gw_me_pw",melee(10, 4, 3, 0, 140))
    wf("gw_mi",missile(5, 2, 3, 0, 135))
 
if __name__ == "__main__":
    # Core
    # Citizen Spears
    cs_chd=lf("cs_chd")
    cs=lf("cs")
    # Highborn Lancers
    hl_chg=lf("hl_chg")
    hl=lf("hl")
    # Ellein Reavers
    er_me_chg=lf("er_me_chg")
    er_me=lf("er_me")
    er_mi=lf("er_mi")
    # Citizen Archers
    ca_me=lf("ca_me")
    ca_mi=lf("ca_mi")
    # Seaguard
    sg_me_chd=lf("sg_me_chd")
    sg_me=lf("sg_me")
    sg_mi=lf("sg_mi")
    
    # Special
    # Sword Masters
    sm=lf("sm")
    # Lion Guard
    lg_mw=lf("lg_mw")
    lg=lf("lg")
    # Flame Wardens
    fw=lf("fw")
    # Knights of Ryma
    kor_chg=lf("kor_chg")
    kor=lf("kor")
    # Reaver Chariots
    rc_me_chg=lf("rc_me_chg")
    rc_me=lf("rc_me")
    rc_mi=lf("rc_mi")
    # Lion Chariot
    lc_chg_mw=lf("lc_chg_mw")
    lc_chg=lf("lc_chg")
    lc_mw=lf("lc_mw")
    lc=lf("lc")
    # Giant Eagles
    ge_st=lf("ge_st")
    ge=lf("ge")
    # Frost Phoenix
    frp_st=lf("frp_st")
    frp_wb_st=lf("frp_wb_st")
    frp=lf("frp")
    frp_wb=lf("frp_wb")
    #Fire Phoenix
    fip_st=lf("fip_st")
    fip_wb_st=lf("fip_wb_st")
    fip=lf("fip")
    fip_wb=lf("fip_wb")
    # Initiate of the Fiercy Heart
    iotfh_st_br=lf("iotfh_st_br")
    iotfh_br=lf("iotfh_br")
    iotfh_st=lf("iotfh_st")
    iotfh=lf("iotfh")
    # Sea Guard Reaper
    sgr_me=lf("sgr_me")
    sgr_mi_1_1=lf("sgr_mi_1_1")
    sgr_mi_1_5=lf("sgr_mi_1_5")
    sgr_mi_6=lf("sgr_mi_6")
    # Sky Sloop
    ss_me_chg=lf("ss_me_chg")
    ss_me=lf("ss_me")
    ss_mi=lf("ss_mi")
    
    # Queen's Bows
    # Queen's Guard
    qg_me=lf("qg_me")
    qg_me_s_chd=lf("qg_me_s_chd")
    qg_me_s=lf("qg_me_s")
    qg_mi=lf("qg_mi")
    # Grey Watchers
    gw_me=lf("gw_me")
    gw_me_pw=lf("gw_me_pw")
    gw_mi=lf("gw_mi")
