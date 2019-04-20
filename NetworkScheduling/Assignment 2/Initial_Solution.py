# -*- coding: utf-8 -*-
"""
Created on Thu Apr 18 11:47:03 2019

@author: hofma
"""

import gurobipy as grb
import csv
from math import *
from Functions import *
from Input import *
from Time_Space import *

GRB = grb.GRB

#Make list of Lf and Lb arc numbers, without fictional arc
Lf = []
for i in range(len(arc_no)-1):
    Lf.append(arc_no[i][0])

Lb = []
for i in range(len(arc_no_bus)):
    Lb.append(arc_no_bus[i][0])

# CREATE MODEL
m = grb.Model('MinAllocCost')

# DECISION VARIABLES
tpre     = {}    #t_p^r,e
tprb     = {}    #t_p^r,b
fik     = {}    #f_i^k
yak      = {}    #y_a^k 

### CREATE INITIAL DECISION VARIABLES ###########################################################################################

#t_p^r for economy
for p in range(len(itinerary_no)):
    r = 771                         #Only spill to fictitious itinerary
    tpre[p,r] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
    name="t_%s^{%s,e}"%(p,r))

#t_p^r for business    
for p in range(len(itinerary_no)):
    r = 771                         #Only spill to fictitious itinerary
    tprb[p,r] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
    name="t_%s^{%s,b}"%(p,r))
    
#f_i^k
for i in Lf:      #Do not take fictitious itinerary into account
    for k in range(len(k_units)):
        fik[i,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
    name="f_%s^{%s}"%(i,k))
        
#y_a^k
for k in range(len(k_units)):
    for a in range(len(arcs[k])):
        yak[a,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
    name="y_%s^{%s}"%(a,k))
        
        
##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum(c(k,i)*fik[i,k] for k in range(len(k_units))) for i in Lf) \
        + grb.quicksum(fare_e(p)*tpre[p,r] for p in range(len(itinerary_no))) \
        + grb.quicksum(fare_b(p)*tprb[p,r] for p in range(len(itinerary_no))) \
        + (24.*4500.)

m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective

m.update()
m.write("model.lp")

print "Objective function created."    
    
##### CONSTRAINTS ########################################################################################################

### 1 ################################################################
print "Constraint 1 loading"

for i in Lf:
    i = int(i)
    m.addConstr(grb.quicksum(fik[i,k] for k in range(len(k_units)))
                            ,GRB.EQUAL,
                                1.)

### 2 ################################################################
print "Constraint 2 loading"



for k in range(len(k_units)):
    Okn_set = []
    for u in range(len(Okn[k])):
        Okn_set.append(Okn[k][u][2])
    Ikn_set = []
    for v in range(len(Ikn[k])):
        Ikn_set.append(Ikn[k][v][2])
    m.addConstr(grb.quicksum(fik[i,k] for i in Okn_set)-grb.quicksum(fik[j,k] for j in Ikn_set),
                            GRB.EQUAL,
                            0.)

Okn_set = [] #Clear list
Ikn_set = [] #Clear list

### 3 ################################################################
print "Constraint 3 loading"

for k in range(len(k_units)):
    NG = [] #Make list of ground arcs per k
    for n in range(len(night_arcs[k])):
        a = night_arcs[k][n][0]
        NG.append(a)
    m.addConstr(grb.quicksum(yak[a,k] for a in NG), #Make constraint per k
                            GRB.LESS_EQUAL,
                                AC_k(k))

NG = [] #Clear list

### 4a ################################################################
print "Constraint 4a loading"

for i in Lf:
    m.addConstr(grb.quicksum((s_k_e(k)*fik[i,k]) for k in range(len(k_units))) \
                + grb.quicksum((delta_i_p(i,p)*tpre[p,r]) for p in range(len(itinerary_no))),
                            GRB.GREATER_EQUAL,
                                Q_i_e(i))
    
### 4b ################################################################
print "Constraint 4b loading"

for i in Lf:
    m.addConstr(grb.quicksum((s_k_b(k)*fik[i,k]) for k in range(len(k_units))) \
                + grb.quicksum((delta_i_p(i,p)*tprb[p,r]) for p in range(len(itinerary_no))),
                            GRB.GREATER_EQUAL,
                                Q_i_b(i))    

### 4c ################################################################
print "Constraint 4c loading"

for i in Lb:
    m.addConstr(216 + grb.quicksum((delta_i_p(i,p)*tpre[p,r]) for p in range(len(itinerary_no))) \
                + grb.quicksum((delta_i_p(i,p)*tprb[p,r]) for p in range(len(itinerary_no))),
                            GRB.GREATER_EQUAL,
                                (Q_i_e(i) + Q_i_b(i)))
    
### Constraints 5a and 5b relaxed in initial solution ###


### Run 
    
m.write("model.lp")
 
m.optimize()    
 
pi = [c.Pi for c in m.getConstrs()]

sigma = pi[len(arc_no):(len(arc_no)+len(itinerary_no))]
pi = pi[:len(arc_no)]
 
c_pi = [pi]

   
for v in m.getVars():
    if v.x > 0:
        print (v.varName, v.x)    
print ('Obj:', m.objVal)

    
    
    
    
    
    
    