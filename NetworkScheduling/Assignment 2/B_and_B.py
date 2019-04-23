# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:51:11 2019

@author: woute
"""

from Iteration import *
import gurobipy as grb

m = grb.Model('MinAllocCost')

# DECISION VARIABLES
tpre     = {}    #t_p^r,e
tprb     = {}    #t_p^r,b
fik     = {}    #f_i^k
yak      = {}    #y_a^k 

### CREATE INITIAL DECISION VARIABLES ###########################################################################################

#t_p^r for economy
for p in range(len(itinerary_no)):
    for r in list(r_obj[p]):
        tpre[p,r] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
        name="t_%s^{%s,e}"%(p,r))
        tpre[r,p] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
        name="t_%s^{%s,e}"%(r,p))
    for r in list(constr_r_a):
        tpre[p,r] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
        name="t_%s^{%s,e}"%(p,r))
        tpre[r,p] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
        name="t_%s^{%s,e}"%(r,p))            

#t_p^r for business    
for p in range(len(itinerary_no)):                        
    tprb[p,771] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, #Only spill business pax to fictitious itinerary
    name="t_%s^{771,b}"%(p))
    
    
#f_i^k
for i in Lfbis:      #Take fictitious itinerary into account
    for k in range(len(k_units)):
        fik[i,k] = m.addVar(vtype=GRB.INTEGER, lb=0,
    name="f_%s^{%s}"%(i,k))
        
#y_a^k
for k in range(len(k_units)):
    for a in range(len(arcs[k])):
        yak[a,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
    name="y_%s^{%s}"%(a,k))
        
m.update()        
##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum(costki(k,i)*fik[i,k] for k in range(len(k_units))) for i in Lfbis) \
+ grb.quicksum(grb.quicksum(((fare_e(p)-(b_p_r(p,r)*fare_e(r)))*tpre[p,r]) for r in list(r_obj[p])) for p in range(len(itinerary_no))) \
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
                + grb.quicksum(grb.quicksum((delta_i_p(i,p)*tpre[p,r]) for p in range(len(itinerary_no))) for r in list(add_col_a[p])) \
                - grb.quicksum(grb.quicksum((delta_i_p(i,p)*b_p_r(r,p)*tpre[r,p]) for p in range(len(itinerary_no))) for r in list(add_col_a[p])),
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
    m.addConstr(216 + grb.quicksum(grb.quicksum((delta_i_p(i,p)*tpre[p,r]) for p in range(len(itinerary_no))) for r in list(add_col_c[p])) \
                - grb.quicksum(grb.quicksum((delta_i_p(i,p)*b_p_r(r,p)*tpre[r,p]) for p in range(len(itinerary_no))) for r in list(add_col_c[p])) + grb.quicksum((delta_i_p(i,p)*tprb[p,771]) for p in range(len(itinerary_no))),
                            GRB.GREATER_EQUAL,
                                (Q_i_e(i) + Q_i_b(i)))
    
### 5a ################################################################
print "Constraint 5a loading"

if len(constr_p_a) > 0.:
    for k in range(len(constr_p_a)):
        p = constr_p_a[k]
        r = constr_r_a[k]
        m.addConstr(grb.quicksum(tpre[p,r] for r in list(r_obj[p])),
                    GRB.LESS_EQUAL,
                    D_p_e(p))
    
### 5b ################################################################
print "Constraint 5b loading"

if len(constr_p_b) > 0.:
    for k in range(len(constr_p_b)):
        p = constr_p_b[k]
        r = constr_r_b[k]
        
        m.addConstr(tprb[p,771],
                GRB.LESS_EQUAL,
                D_p_b(p))

### Run 
m.update()   
m.write("model.lp")

m.optimize()
