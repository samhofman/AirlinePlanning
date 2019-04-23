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



obj_list = []


#Make list of Lf and Lb arc numbers, without fictional arc
Lf = []
for i in range(len(arc_no)-1):
    Lf.append(arc_no[i][0])

Lfbis = []
for i in range(len(arc_no)-1):
    Lfbis.append(arc_no[i][0])
Lfbis.append(232)

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

obj = grb.quicksum(grb.quicksum(costki(k,i)*fik[i,k] for k in range(len(k_units))) for i in Lfbis) \
        + grb.quicksum(fare_e(p)*tpre[p,r] for p in range(len(itinerary_no))) \
        + grb.quicksum(fare_b(p)*tprb[p,r] for p in range(len(itinerary_no))) \
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

#Okn_set = [] #Clear list
#Ikn_set = [] #Clear list

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

#sigma = pi[len(arc_no):(len(arc_no)+len(itinerary_no))]
#pi = pi[:len(arc_no)]
sigma_e = []
sigma_b = []

pi_fe = pi[1880:1880+len(Lf)]
pi_fb = pi[1880+len(Lf):1880+len(Lf)+len(Lf)]
pi_b = pi[1880+len(Lf)+len(Lf):1880+len(Lf)+len(Lf)+len(Lb)] 

c_pi = [pi]

#for var in m.getVars():
#    # Or use list comprehensions instead 
#    if 'f' == str(var.VarName[0]) and var.x > 0:
#        print var.VarName, var.x 

for v in m.getVars():
    if v.x > 0:
        print (v.varName, v.x)    
print ('Obj:', m.objVal)
obj_list.append(m.objVal)



p_sigmae = []
p_sigmab = []
#definition to add column
def add_col(a,p,r,p_sigmae,p_sigmab,sigma_e,sigma_b,pi_fe,pi_fb,pi_b):
    
    tpr_val = 0.
    pi_i = 0.
    pi_j = 0.
    
    #for constraint 4a
    if a == 0:
        for i in range(len(flight_no)-1):
            pi_i = pi_i + delta_i_p(i, p) * pi_fe[i]
            pi_j = pi_j + delta_i_p(i, r) * pi_fe[i]

        if len(p_sigmae) == 0:
            tpr_val = (fare_e(p)-pi_i) - b_p_r(p, r) * (fare_e(r) - pi_j)
        
        else:
            #print 'column'
            for j in range(len(p_sigmae)):
                if p_sigmae[j] == p:
                    #print 'sigma', sigma_e[j]
                    tpr_val = (fare_e(p)-pi_i) - b_p_r(p, r) * (fare_e(r) - pi_j) + sigma_e[j]
    
    #for constraint 4b
    elif a == 1:
        for i in range(len(flight_no)-1):
            pi_i = pi_i + delta_i_p(i, p) * pi_fb[i]
            pi_j = pi_j + delta_i_p(i, r) * pi_fb[i]
    
        if len(p_sigmab) == 0:
            tpr_val = (fare_b(p)-pi_i)
            #tpr = 1 #>0 -> only spill to fictitious
        else:
            #print 'column'
            for j in range(len(p_sigmab)):
                
                if p_sigmab[j] == p:
                    #print 'sigma', sigma_b[j]
                    tpr_val = (fare_b(p)-pi_i) - sigma_b[j]
            #tpr = 1
    #for constraint 4c        
    elif a == 2:
        for i in range(len(flight_no_bus)):
            pi_i = pi_i + delta_i_p(i, p) * pi_b[i]
            pi_j = pi_j + delta_i_p(i, r) * pi_b[i]
    
        if len(p_sigmab) == 0:
            tpr_val = (fare_e(p)-pi_i) - b_p_r(p, r) * (fare_e(r) - pi_j)
        
        else:
            #print 'column'
            for j in range(len(p_sigmae)):
                if p_sigmae[j] == p:
                    #print 'sigma', sigma_e[j]
                    tpr_val = (fare_e(p)-pi_i) - b_p_r(p, r) * (fare_e(r) - pi_j) + sigma_e[j]
    
    
    return tpr_val
    






    
    
    
    
    