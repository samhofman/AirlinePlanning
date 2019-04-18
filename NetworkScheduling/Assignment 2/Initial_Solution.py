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
for i in range(len(arc_no)-1):      #Do not take fictitious itinerary into account
    for k in range(len(k_units)):
        fik[i,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
    name="f_%s^{%s}"%(i,k))
        
#y_a^k
for k in range(len(k_units)):
    for a in range(len(arcs[k])):
        yak[a,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
    name="y_%s^{%s}"%(a,k))
        
##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum(c(k,i)*fik[i,k] for k in range(len(k_units)))for i in range(len(arc_no)-1)) \
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

for i in range(len(arc_no)-1):
    m.addConstr(grb.quicksum(fik[i,k] for k in range(len(k_units)))
                            ,GRB.EQUAL,
                                1.)

### 2 ################################################################
print "Constraint 2 loading"

#for k in range(len(k_units):
#    for n in range(len(time_space[k])):
#        m.addConstr(yak[a,k] + grb.quicksum(fik[i,k] for i ),
#                            GRB.LESS_EQUAL,
#                            D(p, k))
 
m.write("model.lp")
 
m.optimize()    
    
    
    
    
    
    
    
    
    