# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:00:13 2019

@author: woute
"""

import gurobipy as grb
import csv
from math import *
from tableaux_r import *

GRB = grb.GRB

# CREATE MODEL
m = grb.Model('MaxExample')


# DECISION VARIABLES
fraction     = {}    #f_k,p
slack        = {}    #s_i,j

### CREATE DECISION VARIABLES ###########################################################################################
for k in range(len(commodities)):
    for p in range(len(SP[k])):
            fraction[k,p] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                        name="f_%s,%s"%(k,p))

for a in range(len(arcs)):
            slack[a] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                        name="s_%s"%(a))

m.update()

##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum(d(k)*cp(k,p)*fraction[k,p] for p in range(len(SP[k]))) for k in range(len(commodities))) + 1000 * grb.quicksum( sl(a) * slack[a] for a in range(len(arcs)))




m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective

print "Objective function created."


##### CONSTRAINTS ########################################################################################################

### 1 ################################################################
print "Constraint 1 loading"

for a in range(len(arcs)):
    m.addConstr(grb.quicksum(grb.quicksum(d(k)*fraction[k,p]*delta_sp[k][a][p] for p in range(len(SP[k]))) for k in range(len(commodities))) - sl(a) * slack[a],
                            GRB.LESS_EQUAL,
                            u(a))

### 2 ################################################################
print "Constraint 2 loading"

for k in range(len(commodities)):
    m.addConstr(grb.quicksum(fraction[k,p] for p in range(len(SP[k]))),
                            GRB.EQUAL,
                            1)


m.write("model.lp")
 
m.optimize()

for v in m.getVars():
    if v.x > 0:
        print (v.varName, v.x)    
print ('Obj:', m.objVal) 



pi = [c.Pi for c in m.getConstrs()]

sigma = pi[len(arcs):(len(arcs)+len(commodities))]
pi = pi[:len(arcs)]
    
c_sigma = [sigma]
c_pi = [pi]


slack_row = []

for a in range(len(arcs)):
    if sl(a) == 0.:
        slack_row.append(0)
    if sl(a) == 1.:
        slack_row.append(1)
        





