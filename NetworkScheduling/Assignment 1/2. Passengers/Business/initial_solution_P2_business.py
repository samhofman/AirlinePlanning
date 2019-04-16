# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:00:13 2019

@author: woute
"""

import gurobipy as grb
import csv
from math import *
from tableaux_P2_business import *
from Functions_P2_business import *

GRB = grb.GRB


# CREATE MODEL
m = grb.Model('MinPaxCost')


# DECISION VARIABLES
reallo     = {}    #t_p^r,k

### CREATE INITIAL DECISION VARIABLES ###########################################################################################

for p in range(len(itinerary_no)):
    r = 737
    k = 1
    reallo[p,r,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
name="t_%s^{%s,%s}"%(p,r,k))



##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(path_fare(p, k) * reallo[p,r,k] for p in range(len(itinerary_no)))



m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective

m.update()
m.write("model.lp")


print "Objective function created."


##### CONSTRAINTS ########################################################################################################

### 1 ################################################################
print "Constraint 1 loading"

for f in range(len(flight_no)):
    k = 1
    m.addConstr(grb.quicksum(delta(f,p)*reallo[p,r,k] for p in range(len(itinerary_no)))# - grb.quicksum(delta(f,p)*recap_rate(p,r,k)*reallo[p,r,k] for p in range(len(itinerary_no)))
                        ,GRB.GREATER_EQUAL,
                            Q_CAP(f,k))

### 2 ################################################################
print "Constraint 2 loading"

for p in range(len(itinerary_no)):
    k = 1
    m.addConstr(reallo[p,r,k],
                            GRB.LESS_EQUAL,
                            D(p, k))
 
m.write("model.lp")
 
m.optimize()


pi = [c.Pi for c in m.getConstrs()]

sigma = pi[len(flight_no):(len(flight_no)+len(itinerary_no))]
pi = pi[:len(flight_no)]
 
c_pi = [pi]

   
for v in m.getVars():
    if v.x > 0:
        print (v.varName, v.x)    
print ('Obj:', m.objVal)


tableau = {}


for p in range(len(itinerary_no)):
    tableau[p] = np.zeros((1,1))

for p in range(len(itinerary_no)):
    if reallo[p,737,1].x > 0:
        tableau[p][0][0] = 1
    


def add_col_init(p,r):
    pi_i = 0.
    pi_j = 0.
    
    for f in range(len(flight_no)):
        pi_i = pi_i + delta(f, p) * pi[f]
        pi_j = pi_j + delta(f, r) * pi[f]
    
    if len(sigma) == 0:
        tpr = (path_fare(p,1)-pi_i) - recap_rate(p, r, 1) * (path_fare(r, k) - pi_j)
    
    else:
        tpr = (path_fare(p,1)-pi_i) - recap_rate(p, r, 1) * (path_fare(r, k) - pi_j) - sigma[p]
    
    return tpr
#
#i = 0
#p_list = []
#r_list = [737]
#for p in range(len(itinerary_no)):
#    for c in range(len(recapture_from_to)):
#        if p == recapture_from_to[c][0]:
#            if add_col_init(p, recapture_from_to[c][1]) < 0. :
#                col = {}
#                col[0] = np.zeros((1,1))
#                col[0][0][0] = 1.
#                tableau[p] = np.hstack((tableau[p],col[0]))
#                
#                p_list.append(p)
#                r_list.append(recapture_from_to[c][1])
#                
#                i = i + 1


#columns = {}
#
#for p in range(len(itinerary_no)):
#    columns[p] = [737]
#    for c in range(len(recapture_from_to)):
#        if p == recapture_from_to[c][0]:
#            if add_col_init(p, recapture_from_to[c][1]) < 0. :
#                columns[p].append(recapture_from_to[c][1])
            













