# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:00:13 2019

@author: woute
"""

import gurobipy as grb
import csv
from math import *
from tableaux2 import *
from Functions import *

GRB = grb.GRB



### Initial Tableau ###
#
#delta_init = {}
#
#for p in range(len(itinerary_no)):
#    delta_init[p] = np.zeros((len(flight_no),1))
#
#for p in range(len(itinerary_no)):
#    for f in range(len(flight_no)):
#        delta_init[p][f] = delta(f,p)
#
#for i in range(len(delta_init[0])):
#    if delta_init[0][i] > 0.:
#        print i, delta_init[0][i]


# CREATE MODEL
m = grb.Model('MinPaxCost')


# DECISION VARIABLES
reallo     = {}    #t_p^r,k

### CREATE DECISION VARIABLES ###########################################################################################
for p in range(len(itinerary_no)):
    r = 0
    for k in range(2):
        reallo[p,r,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
name="t_%s^{%s,%s}"%(p,r,k))





##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum(fare[p][k] * reallo[p,r,k] for k in range(2)) for p in range(len(itinerary_no)))



m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective

m.update()
m.write("model.lp")


print "Objective function created."


##### CONSTRAINTS ########################################################################################################

### 1 ################################################################
print "Constraint 1 loading"

for f in range(len(flight_no)):
    k = 1.
    m.addConstr(grb.quicksum(delta(f,p)*reallo[p,r,k] for p in range(len(itinerary_no)))# - grb.quicksum(delta(f,p)*recap_rate(p,r,k)*reallo[p,r,k] for p in range(len(itinerary_no)))
                        ,GRB.GREATER_EQUAL,
                            Q_CAP(f,k))

### 2 ################################################################
#print "Constraint 2 loading"

#for p in range(len(itinerary_no)):
#    for k in range(2):
#        m.addConstr(reallo[p,r,k],
#                            GRB.LESS_EQUAL,
#                            D(p, k))
 
#for a in range(len(arcs)):
#    m.addConstr(slack[a], 
#                GRB.EQUAL, 
#                max{0,grb.quicksum(grb.quicksum(d(k)*fraction[k,p]*delta(k,p,arcs[i][1],arcs[i][2]) for p in range(len(P[k]))) for k in range(len(commodities))) - u(a)} )
    


m.write("model.lp")
 
m.optimize()


pi = [c.Pi for c in m.getConstrs()]

sigma = pi[len(flight_no):(len(flight_no)+len(itinerary_no))]
pi = pi[:len(flight_no)]
    
for v in m.getVars():
    if v.x > 0:
        print (v.varName, v.x)    
print ('Obj:', m.objVal)


business_cost = 0.

for p in range(len(itinerary_no)):
    business_cost = business_cost + path_fare(p, 1) * reallo[p, 0, 1].x


tableau = {}









for p in range(len(itinerary_no)):
    tableau[p] = np.zeros((len(flight_no),1))

for p in range(len(itinerary_no)):
    for r in range(1):
        for f in range(len(flight_no)):
            if reallo[p,0,0].x > 0:
                tableau[p][f][r] = delta(f, p)
    


    




 





















