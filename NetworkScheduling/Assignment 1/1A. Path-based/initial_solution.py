# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:00:13 2019

@author: woute
"""

import gurobipy as grb
import csv
from math import *
from tableaux import *

GRB = grb.GRB

# CREATE MODEL
m = grb.Model('MaxExample')


# DECISION VARIABLES
fraction     = {}    #f_k,p
slack        = {}    #s_i,j

### CREATE DECISION VARIABLES ###########################################################################################
for k in range(len(commodities)):
    for p in range(len(P[k])):
            fraction[k,p] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                        name="f_%s,%s"%(k,p))

for a in range(len(arcs)):
            slack[a] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="s_%s"%(a))

m.update()

##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum(d(k)*cp(k,p)*fraction[k,p] for p in range(1)) for k in range(len(commodities))) + 1000 * grb.quicksum(slack[a] for a in range(len(arcs)))




m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective

print "Objective function created."


##### CONSTRAINTS ########################################################################################################

### 1 ################################################################
print "Constraint 1 loading"

for i in range(len(arcs)):
    m.addConstr(grb.quicksum(grb.quicksum(d(k)*fraction[k,p]*delta(k,p,i) for p in range(1)) for k in range(len(commodities))) - slack[i],
                            GRB.LESS_EQUAL,
                            u(i))

### 2 ################################################################
print "Constraint 2 loading"

for k in range(len(commodities)):
    m.addConstr(grb.quicksum(fraction[k,p] for p in range(1)),
                            GRB.EQUAL,
                            1)
 
#for a in range(len(arcs)):
#    m.addConstr(slack[a], 
#                GRB.EQUAL, 
#                max{0,grb.quicksum(grb.quicksum(d(k)*fraction[k,p]*delta(k,p,arcs[i][1],arcs[i][2]) for p in range(len(P[k]))) for k in range(len(commodities))) - u(a)} )
    


m.write("model.lp")
 
m.optimize()


pi = [c.Pi for c in m.getConstrs()]

sigma = pi[len(arcs):(len(arcs)+len(commodities))]
pi = pi[:len(arcs)]
    
for v in m.getVars():
    if v.x > 0:
        print (v.varName, v.x)    
print ('Obj:', m.objVal) 



 





















