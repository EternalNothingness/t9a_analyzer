# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 13:46:46 2023

@author: pwint
"""
import copy as c
import numpy as np
#import pathlib as pl
import pprint as pp

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

def show_me(l1):
    l2=c.copy(np.array(l1).round(2).tolist())
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
            ltemp+=c.copy(l2[i+35*j])
        ltest.append(ltemp)
        string=6*"{: >7} {: >5} {: >5} {: >5} {: >5} "
    for row in ltest:
        print(string.format(*row))
       
def show_mi(lret):
    ranint=[]
    for i in range(0,len(lret),175):
        ranint.append(lret[i][0])
    ltest=[['','','','']+['','','','']+['','','','']+['','','','']+['Range','0','-',ranint[0]]]
    ltest.append(['','','','Normal']+['','Move','and','Shoot']+['','Stand','and','Shoot']+['','','Soft','Cover']+['','','Hard','Cover'])
    ltest.append(5*["res","arm","dmg","norm"])
    for k in range(len(ranint)):
        # get block of data in same range
        lround=np.array(lret)[k*int(len(lret)/len(ranint)):(k+1)*int(len(lret)/len(ranint))].round(2).tolist()
        for i in range(int(len(lret)/len(ranint)/5)):
            ltemp=[]
            if i%7 == 0 and (i!=0 or k!=0):
                ltest.append(5*['','','','',''])
            if int(i%(len(lret)/len(ranint)))==0 and k!=0:
                ltest.append(['','','','']+['','','','']+['','','','']+['','','','']+['Range',ranint[k-1],'-',ranint[k]])
                ltest.append(['','','','Normal']+['','Move','and','Shoot']+['','Stand','and','Shoot']+['','','Soft','Cover']+['','','Hard','Cover'])
                ltest.append(5*["res","arm","dmg","norm"])
            for j in range(5):
                ltemp+=lround[i+int(len(lround)/5)*j][1:]
            ltest.append(ltemp)
    string=5*"{: >7} {: >5} {: >5} {: >5} "
    for row in ltest:
        print(string.format(*row))

# treat breath as an additional modelpart with 0 attack and auto hits
def melee(att,off,_str,ap,pt,mw=1,autohits=0,hmod=0,wmod=0,test=False):
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
                l2.append([_def,res,arm,dmg,dmgpt])
    if test==True:
        show_me(l2)
    else:
        return l2

def missile(ran,att,aim,_str,ap,pt,mw=1,aa=1,acc=False,qtf=False,unw=False,mof=False,sta=False,rel=False,test=False):
    l2=[]   
    if type(att)==list: # extend optional parameters to lists
        if type(mw)!=list:
            mw=[mw for i in range(len(att))]
        if type(aa)!=list:
            aa=[aa for i in range(len(att))]
    aim_orig=aim
    for i in range(2):
        aim=aim_orig
        # i=0 Short Range, i=1 Long Range
        if i== 1 and acc==False:
            aim+=1
        aim_ran=aim
        for j in range(5):
            aim=aim_ran
            # if j==0:
                # Normal, nothing to do
            # Move and Shoot
            if j==1 and mof==True: # Move or Fire
                aim=90
            elif j==1 and ((qtf==False and unw==False) or (qtf==True and unw==True)): # qick to fire <=> unwieldy
                aim+=1
            elif j==1 and (qtf==False and unw==True): # only unwieldy
                aim+=2 
            # Stand and Shoot
            elif j==2 and rel==True: # Reload!
                aim=90
            elif j==2 and sta==False:
                aim+=1
            # Soft Cover
            elif j==3:
                aim+=1
            # Hard Cover
            elif j==4:
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
                    l2.append([ran/(2-i),res,arm,dmg,dmgpt])
    if test==True:
        show_mi(l2)
    else:
        return l2

def filter2_me(l,_def=-1,res=-1,arm=-1,test=False):
    lc=c.copy(l)
    lret=[]
    for i in range(len(lc)):
        if (lc[i][0]==_def or _def==-1) and (lc[i][1]==res or res==-1) and (lc[i][2]==arm or arm==-1):
            lret.append(lc[i])
    if test==True:
        ltest=[["def","res","arm","dmg","norm"]]
        ltest.extend(np.array(lret).round(2).tolist())
        for row in ltest:
            print("{: >5} {: >5} {: >5} {: >5} {: >5}".format(*row))
    else:
        return lret
    
def filter2_mi(l,res=-1,arm=-1,test=False):
    lc=c.copy(l)
    lret=[]
    for i in range(len(lc)):
        if (lc[i][1]==res or res==-1) and (lc[i][2]==arm or arm==-1):
            lret.append(lc[i])
    if test==True:
        show_mi(lret)
    else:
        return lret
    
def compare2_me(l1,l2,test=False):
    arra=np.array(l1)[:,3:] # get dmg and norm from l1
    arrb=np.array(l2)[:,3:] # get dmg and norm from l2
    if (arrb>0).all:
        arrc=(arra/arrb).copy() # calculates relative dmg/norm
        arrc=np.concatenate((np.array(l1)[:,:3],arrc),1)
        lret = arrc.tolist()
        if test==True:
            show_me(lret)
        else:
            return lret
        
def compare2_mi(l1,l2,test=False):
    arra=np.array(l1)[:,3:] # get dmg and norm from l1
    arrb=np.array(l2)[:,3:] # get dmg and norm from l2
    ranint=np.sort(np.array([l1[0][0],l1[-1][0],l2[0][0],l2[-1][0]])).tolist() # range intervals
    for i in ranint:
        if ranint.count(i)>1: # remove redunant numbers
            ranint.remove(i)
    #print(ranint)
    aret=np.array([0 for i in range(5)])[None,:] # placeholder
    for i in ranint: # range intervals
        if l1[0][0]>=i: # Short Range
            if l2[0][0]>=i: # Short Range
                atemp=np.concatenate(([[i] for j in range(int(len(l1)/2))],np.array(l1)[:int(len(l1)/2),1:3],arra[:int(len(l1)/2)]/arrb[:int(len(l1)/2)]),1)
            elif l2[-1][0]>=i: # Long Range
                atemp=np.concatenate(([[i] for j in range(int(len(l1)/2))],np.array(l1)[:int(len(l1)/2),1:3],arra[:int(len(l1)/2)]/arrb[int(len(l1)/2):]),1)
            else: # Not in Range
                atemp=np.concatenate(([[i] for j in range(int(len(l1)/2))],np.array(l1)[:int(len(l1)/2),1:3],arra[:int(len(l1)/2)]/np.array([[0,0] for i in range(int(len(l1)/2))])),1)
        elif l1[-1][0]>=i: # Long Range
            if l2[0][0]>=i: # Short Range
                atemp=np.concatenate(([[i] for j in range(int(len(l1)/2))],np.array(l1)[:int(len(l1)/2),1:3],arra[int(len(l1)/2):]/arrb[:int(len(l1)/2)]),1)
            elif l2[-1][0]>=i: # Long Range
                atemp=np.concatenate(([[i] for j in range(int(len(l1)/2))],np.array(l1)[:int(len(l1)/2),1:3],arra[int(len(l1)/2):]/arrb[int(len(l1)/2):]),1)
            else: # Not in Range
                atemp=np.concatenate(([[i] for j in range(int(len(l1)/2))],np.array(l1)[:int(len(l1)/2),1:3],arra[int(len(l1)/2):]/np.array([[0,0] for i in range(int(len(l1)/2))])),1)
        else: # Not in Range
            if l2[0][0]>=i: # Short Range
                atemp=np.concatenate(([[i] for j in range(int(len(l1)/2))],np.array(l1)[:int(len(l1)/2),1:3],np.array([[0,0] for i in range(int(len(l1)/2))])/arrb[:int(len(l1)/2)]),1)
            elif l2[-1][0]>=i: # Long Range
                atemp=np.concatenate(([[i] for j in range(int(len(l1)/2))],np.array(l1)[:int(len(l1)/2),1:3],np.array([[0,0] for i in range(int(len(l1)/2))])/arrb[int(len(l1)/2):]),1)
            else: # Not in Range
                atemp=np.concatenate(([[i] for j in range(int(len(l1)/2))],np.array(l1)[:int(len(l1)/2),1:3],np.array([[0,0] for i in range(int(len(l1)/2))])/np.array([[0,0] for i in range(int(len(l1)/2))])),1)
        aret=np.concatenate((aret,atemp))
    lret = aret.tolist()[1:] # remove placeholder
    if test==True:
        show_mi(lret)
    else:
        return lret
    
def sorteff(l1,test=False):
    order=np.array(l1)[:,4].argsort(0)
    lret=[]
    for i in range(len(l1)):
        lret.append(l1[order[i]])
    lret=np.array(lret)[::-1,:].tolist()
    if test==True:
        show_me(lret)
    else:
        return lret

def compare_me(l1,l2,test=False):
    lnorm=np.array([[] for i in range(len(l1[0]))])
    for mat in l1:
        lnorm=np.concatenate((lnorm,np.array(mat)[:,4,None]),1)
    order=lnorm.argsort()
    order3=np.array([[] for i in range(len(l1[0]))])
    for i in range(len(l1)): # len(l1)=number of units
        order3=np.concatenate((order3, order[:,i,None], order[:,i,None],order[:,i,None]),1)
    order3=order3[:,::-1].tolist() # reverse order (best unit first)
    lret=np.concatenate((np.array(l1)[0,:,:3],np.array(order3)),1).tolist()
    for i in range(len(lret)):
        for j in range(len(l1)): # len(l1)=number of units
            lret[i][3+3*j]=l2[int(order3[i][3*j])]
            lret[i][3+3*j+1]=l1[int(order3[i][3*j+1])][i][3]
            lret[i][3+3*j+2]=(np.array(l1[int(order3[i][3*j+2])][i][4])/np.array(l1[int(order3[i][3*0+2])][i][4])).tolist() # determine cost effectiveness
    if test==True:
        ltemp=np.array([[] for i in range(len(l1[0]))])
        for i in range(len(lret[0])):
            if type(lret[0][i])==str: # test if rounding is sensible
                ltemp=np.concatenate((ltemp,np.array(lret)[:,i,None]),1)
            else: # double array because of type conv
                ltemp=np.concatenate((ltemp,np.array(np.array(lret)[:,i,None],dtype='float64').round(2)),1)
        
        ltest=[["def","res","arm"]]
        ltest[0].extend(len(l1)*["unit","dmg","eff"])
        ltest.extend(ltemp)
        dist=0 # distance between unit columns
        for string in l2:
            dist=max(dist,len(string))
        dist+=5
        string="{: >5} {: >5} {: >5}"+len(l1)*(" {: >%d} {: >5} {: >5}" %dist)
        k=0
        for row in ltest:
            print(string.format(*row))
            if k%7==0 and k!=0:
                print()
            k+=1
    else:
        return lret
    
def filter_me(l,_def=-1,res=-1,arm=-1,test=False):
    lret=[]
    for i in range(len(lc)):
        if (l[i][0]==_def or _def==-1) and (l[i][1]==res or res==-1) and (l[i][2]==arm or arm==-1):
            lret.append(l[i])
    if test==True:
        ltest=[["def","res","arm"]]
        ltest[0].extend(int((len(l[0])-3)/3)*["unit","dmg","eff"])
        ltemp=np.array([[] for i in range(len(lret))])
        lstr=np.array([[] for i in range(len(lret))]) # list of all unit names
        for i in range(len(lret[0])):
            if type(lret[0][i])==str: # test if rounding is sensible
                ltemp=np.concatenate((ltemp,np.array(lret)[:,i,None]),1)
                lstr=np.concatenate((lstr,np.array(lret)[:,i,None]),1)
            else: # double array because of type conv
                ltemp=np.concatenate((ltemp,np.array(np.array(lret)[:,i,None],dtype='float64').round(2)),1)
        ltest.extend(ltemp)
        dist=0 # distance between unit columns
        for string in lstr.flatten().tolist():
            dist=max(dist,len(string))
        dist+=5
        string="{: >5} {: >5} {: >5}"+int((len(l[0])-3)/3)*(" {: >%d} {: >5} {: >5}" %dist)
        for row in ltest:
            print(string.format(*row))
    else:
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
    wf("er_mi",missile(24,5,3,3,0,180))
    # Citizen Archers
    wf("ca_me",melee(10, 4, 3, 0, 150, hmod=1))
    wf("ca_mi",missile(30,10, 3, 3, 0, 150,acc=True))
    # Seaguard
    wf("sg_me_chd",melee(15, 4, 3, 2, 240, hmod=1))
    wf("sg_me",melee(15, 4, 3, 1, 240, hmod=1))
    wf("sg_mi",missile(24,15, 3, 3, 0, 240,sta=True))
    
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
    wf("rc_me_chg",melee([2,2,0], [4,3,0], [4,3,5], [1,0,2], 110, autohits=[0,0,3.5], hmod=[1,0,0]))
    wf("rc_me",melee([2,2,0], [4,3,0], [3,3,5], [0,0,2], 110, hmod=[1,0,0]))
    wf("rc_mi",missile(30,2, 3, 3, 0, 90))
    # Lion Chariot
    wf("lc_chg_mw",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195, mw=[2,1,1], autohits=[0,0,4.5]))
    wf("lc_chg",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195, autohits=[0,0,4.5]))
    wf("lc_mw",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195, mw=[2,1,1]))
    wf("lc",melee([2,4,0], [5,5,0], [6,5,5], [3,2,2], 195))
    # Giant Eagles
    wf("ge_st",melee(2, 5, 4, 1, 100,autohits=1)) # Large => stomp(1)
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
    wf("iotfh_st",melee([1,4], [4,5], [3,5], [0,2], 330, autohits=[0,1], hmod=[1,0])) # Large => stomp(1)
    wf("iotfh",melee([1,4], [4,5], [3,5], [0,2], 330, hmod=[1,0]))
    # Sea Guard Reaper
    wf("sgr_me",melee(2, 4, 3, 0, 190,hmod=1))
    wf("sgr_mi_1_1",missile(48,1, 3, 6, 10, 190,mw=2,mof=True,rel=True))
    wf("sgr_mi_1_5",missile(48,[1,1], 3, [3,6], [10,10], 190,mw=[1,1],aa=[4,1],mof=True,rel=True)) # mw=1 is more realistic
    wf("sgr_mi_6",missile(48,6, 3, 4, 2, 190,mof=True,rel=True))
    # Sky Sloop
    wf("ss_me_chg",melee([2,2,0],[4,4,0],[4,4,5],[1,1,2],225,autohits=[0,0,3.5],hmod=[1,0,0]))
    wf("ss_me",melee([2,2,0],[4,4,0],[3,4,5],[0,1,2],225,hmod=[1,0,0]))
    wf("ss_mi",missile(24,4,3,5,3,225,qtf=True,rel=True))
    
    # Queen's Bows
    # Queen's Guard
    wf("qg_me",melee(5, 5, 3, 0, 135,hmod=1))
    wf("qg_me_s_chd",melee(5, 5, 3, 2, 140,hmod=1))
    wf("qg_me_s",melee(5, 5, 3, 1, 140,hmod=1))
    wf("qg_mi",missile(30,5, 2, 4, 1, 135))
    # Grey Watchers
    wf("gw_me",melee(5, 4, 3, 0, 135))
    wf("gw_me_pw",melee(10, 4, 3, 0, 140))
    wf("gw_mi",missile(30,5, 2, 3, 0, 135,acc=True))
 
if __name__ == "__main__":
    wr_he()
    
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
