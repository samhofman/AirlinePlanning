# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 15:19:34 2019

@author: woute
"""

import gurobipy as grb
from tableaux2 import *
from Functions import *
from initial_solution2 import tableau, pi, sigma, r_list, columns, p_list
from next_solution import r_row, p_row, pi, sigma


GRB = grb.GRB

# CREATE MODEL
m = grb.Model('row')


# DECISION VARIABLES
reallo     = {}    #t_p^r,k

### CREATE DECISION VARIABLES ###########################################################################################
for p in range(len(itinerary_no)):
    for r in list(columns[p]):
        k = 0
        reallo[p,r,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
              name="t_%s^{%s,%s}"%(p,r,k))                
#        else:
#            r = 737
#            k = 0
#            reallo[p,r,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
#                      name="t_%s^{%s,%s}"%(p,r,k))




##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum((path_fare(p, k) - recap_rate(p, r, k) * path_fare(r, k)) * reallo[p,r,k] for r in list(columns[p])) for p in range(len(itinerary_no)))



m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective

m.update()
m.write("model.lp")


print "Objective function created."


##### CONSTRAINTS ########################################################################################################

### 1 ################################################################
print "Constraint 1 loading"

for f in range(len(flight_no)):
    k = 0
    m.addConstr(grb.quicksum(grb.quicksum(delta(f,p)*reallo[p,r,k] for r in list(columns[p])) for p in range(len(itinerary_no))) - grb.quicksum(grb.quicksum(delta(f,p)*recap_rate(p,r,k)*reallo[p,r,k] for r in list(columns[p]))for p in range(len(itinerary_no)))
                        ,GRB.GREATER_EQUAL,
                            Q_CAP(f,k))

### 2 ################################################################
print "Constraint 2 loading"

for p in list(p_row):
    r = r_row[p_row.index(p)]
    m.addConstr(reallo[p,r,0],
                            GRB.LESS_EQUAL,
                            D(p, 0))
 



m.write("model.lp")
 
m.optimize()


pi = [c.Pi for c in m.getConstrs()]

sigma = pi[len(flight_no):(len(flight_no)+len(itinerary_no))]
pi = pi[:len(flight_no)]
    
for v in m.getVars():
    if v.x > 0:
        print (v.varName, v.x)    
print ('Obj:', m.objVal)



### ADD ROWS ###

p_row = []
r_row = []
for p in list(recapture_from):
    for r in list(columns[p]):
        if reallo[p,r,0].x > D(p, 0) and r != 737:
            print p,r
            p_row.append(p)
            r_row.append(r)