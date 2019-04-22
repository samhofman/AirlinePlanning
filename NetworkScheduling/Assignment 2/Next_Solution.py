# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 10:16:48 2019

@author: hofma
"""

import gurobipy as grb
import csv
from math import *
from Functions import *
from Input import *
from Time_Space import *
from Initial_Solution import Lf, Lfbis, Lb

GRB = grb.GRB

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
    for r in range(len(itinerary_no)):
        tpre[p,r] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
        name="t_%s^{%s,e}"%(p,r))

#t_p^r for business    
for p in range(len(itinerary_no)):                        
    tprb[p,771] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, #Only spill business pax to fictitious itinerary
    name="t_%s^{771,b}"%(p))
    
#f_i^k
for i in Lfbis:      #Take fictitious itinerary into account
    for k in range(len(k_units)):
        fik[i,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
    name="f_%s^{%s}"%(i,k))
        
#y_a^k
for k in range(len(k_units)):
    for a in range(len(arcs[k])):
        yak[a,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
    name="y_%s^{%s}"%(a,k))
        
        
##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum(c(k,i)*fik[i,k] for k in range(len(k_units))) for i in Lfbis) \
        + grb.quicksum(grb.quicksum(((fare_e(p)-(b_p_r(p,r)*fare_e(r)))*tpre[p,r]) for r in range(len(itinerary_no))) for p in range(len(itinerary_no))) \
        + grb.quicksum(fare_b(p)*tprb[p,771] for p in range(len(itinerary_no))) \
        + (24.*4500.)

m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective

m.update()
m.write("model.lp")

print "Objective function created."    
    
##### CONSTRAINTS ########################################################################################################

### 1a ################################################################
print "Constraint 1a loading"

for i in Lf:
    m.addConstr(grb.quicksum(fik[i,k] for k in range(len(k_units)))
                            ,GRB.EQUAL,
                                1.)

### 1b ################################################################
print "Constraint 1b loading"

for k in range(len(k_units)):
    i = 232
    m.addConstr(fik[i,k]
                            ,GRB.EQUAL,
                                0.)

### 2 ################################################################
print "Constraint 2 loading"

for k in range(len(k_units)):
    for n in range(len(Ikn_set[k])):
        m.addConstr(yak[n,k] + fik[Okn_set[k][n],k] - yak[terminating_arc(n,k),k] - fik[Ikn_set[k][n],k],
                    GRB.EQUAL,
                    0.)

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
                + grb.quicksum(grb.quicksum((delta_i_p(i,p)*tpre[p,r]) for p in range(len(itinerary_no))) for r in range(len(itinerary_no))) \
                - grb.quicksum(grb.quicksum((delta_i_p(i,p)*b_p_r(r,p)*tpre[r,p]) for p in range(len(itinerary_no))) for r in range(len(itinerary_no))),
                            GRB.GREATER_EQUAL,
                                Q_i_e(i))
    
### 4b ################################################################
print "Constraint 4b loading"

for i in Lf:
    m.addConstr(grb.quicksum((s_k_b(k)*fik[i,k]) for k in range(len(k_units))) \
                + grb.quicksum((delta_i_p(i,p)*tprb[p,771]) for p in range(len(itinerary_no))),
                            GRB.GREATER_EQUAL,
                                Q_i_b(i))    

### 4c ################################################################
print "Constraint 4c loading"

for i in Lb:
    m.addConstr(216 + grb.quicksum(grb.quicksum((delta_i_p(i,p)*tpre[p,r]) for p in range(len(itinerary_no))) for r in range(len(itinerary_no))) \
                - grb.quicksum(grb.quicksum((delta_i_p(i,p)*b_p_r(r,p)*tpre[r,p]) for p in range(len(itinerary_no))) for r in range(len(itinerary_no))) \ 
                + grb.quicksum((delta_i_p(i,p)*tprb[p,771]) for p in range(len(itinerary_no))),
                            GRB.GREATER_EQUAL,
                                (Q_i_e(i) + Q_i_b(i)))
    
### 5a ################################################################
print "Constraint 5a loading"

for p in range(len(itinerary_no)):
    m.addConstr(grb.quicksum(tpre[p,r] for r in range(len(itinerary_no))),
                GRB.LESS_EQUAL,
                D_p_e(p))
    
### 5b ################################################################
print "Constraint 5b loading"

for p in range(len(itinerary_no)):
    m.addConstr(tprb[p,771],
                GRB.LESS_EQUAL,
                D_p_b(p))

### Run 
    
m.write("model.lp")
 
#m.optimize()    
 
#pi = [c.Pi for c in m.getConstrs()]
#
#sigma = pi[len(arc_no):(len(arc_no)+len(itinerary_no))]
#pi = pi[:len(arc_no)]
# 
#c_pi = [pi]
#
##for var in m.getVars():
##    # Or use list comprehensions instead 
##    if 'f' == str(var.VarName[0]) and var.x > 0:
##        print var.VarName, var.x 
#
#for v in m.getVars():
#    if v.x > 0:
#        print (v.varName, v.x)    
#print ('Obj:', m.objVal)