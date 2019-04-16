# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:49:08 2019

@author: hofma
"""

import gurobipy as grb
from math import *
import csv

from Functions_P1A import *

GRB = grb.GRB

# CREATE MODEL
m = grb.Model('MaxProfit')


# DECISION VARIABLES
flow     = {}    #x_i,j_k

### CREATE DECISION VARIABLES ###########################################################################################
for i in range(airports):
    for j in range(airports):
        for k in range(len(commodities)):
            flow[i,j,k] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="x_%s,%s_%s"%(i,j,k))


m.update()

##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum(grb.quicksum((c(i,j)*flow[i,j,k]) for i in range(airports)) for j in range(airports)) for k in range(len(commodities)))

m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective

print "Objective function created."

##### CONSTRAINTS ########################################################################################################

### 1 ################################################################
print "Constraint 1 loading"
for i in range(airports):
    for j in range(airports):
        for k in range(len(commodities)):
            m.addConstr((grb.quicksum( flow[i,j,k] for j in range(airports)) - grb.quicksum(flow[j,i,k] for j in range(airports))),
                        GRB.EQUAL,
                        d(i,k))
            
### 2 ################################################################
print "Constraint 2 loading"
for i in range(airports):
    for j in range(airports):
        for k in range(len(commodities)):
            m.addConstr(    grb.quicksum((flow[i,j,k]) for k in range(len(commodities))), 
                        GRB.LESS_EQUAL, 
                        u(i,j))
            
### 3 ################################################################
print "Constraint 3 loading"
for i in range(airports):
    for j in range(airports):
        for k in range(len(commodities)):
            m.addConstr(    flow[i,j,k], 
                        GRB.GREATER_EQUAL, 
                        0.0)
            
m.update()

### RUN ###

def mycallback(model, where):
    if where == GRB.Callback.MIP:
        objbnd = model.cbGet(GRB.Callback.MIP_OBJBND)
        objbst = model.cbGet(GRB.Callback.MIP_OBJBST)
        runtime = model.cbGet(GRB.Callback.RUNTIME)
        if runtime > 60:
            model.terminate()
        elif abs(objbst - objbnd) <= 0.0020 * (abs(objbst)):
            print('Stop early - 0.20% gap achieved')
            model.terminate()
            
            return;
   
m.optimize(mycallback)

                 
for v in m.getVars():
    if v.x > 0:
        print (v.varName, v.x)    
print ('Obj:', m.objVal) 

if m.SolCount == 0:
    print("Model has no solution")
    exit(1)

var_x = []    


for var in m.getVars():
    # Or use list comprehensions instead 
    if 'x' == str(var.VarName[0]) and var.x > 0:
        var_x.append([var.VarName, var.x])
   
# Write to csv
with open('Out_P1.csv', 'wb') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerows(var_x)
