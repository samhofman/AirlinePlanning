# -*- coding: utf-8 -*-
"""
Created on Wed Dec 05 17:16:14 2018

@author: woute
"""
import gurobipy as grb
from functions import *
from math import *

GRB = grb.GRB


# CREATE MODEL
m = grb.Model('MaxProfit')


# DECISION VARIABLES
flow     = {}    #x_i,j
hflow    = {}    #w_i,j
flights  = {}    #z_i,j_k
#aircraft = {}    #AC_k



### CREATE DECISION VARIABLES
for i in range(nodes):
    for j in range(nodes):
        flow[i,j] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="x_%s,%s"%(i,j))
        hflow[i,j] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="w_%s,%s"%(i,j))
        
        for k in range(commod):
            flights[i,j,k] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="z_%s,%s_%s"%(i,j,k))
            #aircraft[k] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        #name="AC_%s"%(k))

m.update()


##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum( (5.9*dist_fact(i,j)+0.043)*distance(i,j)*(hflow[i,j]+flow[i,j]) -  grb.quicksum((Cl[0][k]+cost_fact(i,j)*(CX(i,j,k)+Ct[0][k]*distance(i,j)/speed[0][k]+Cf[0][k]*flights[i,j,k]*distance(i,j)/1.5)) for k in range(commod))for j in range(nodes))for i in range(nodes))

m.setObjective(obj,GRB.MAXIMIZE) #fill in obj instead of m.getObjective


##### CONSTRAINTS ###############################################################################################

### 1 ###
for i in range(nodes):
    for j in range(nodes):
        m.addConstr(flow[i,j] + hflow[i,j], GRB.LESS_EQUAL, demand(i,j))

### 2 ###
for i in range(nodes):
    for j in range(nodes):
        m.addConstr(    hflow[i,j], 
                        GRB.LESS_EQUAL, 
                        demand(i,j)*hub(i)*hub(j))

### 3 ###            
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(flow[i,j]+grb.quicksum((hflow[i,m]*(1-hub(j)))for m in range(nodes))+grb.quicksum((hflow[m,j]*(1-hub(i)))for m in range(nodes)),
                        GRB.LESS_EQUAL, 
                        grb.quicksum((flights[i,j,k]*seats[0][k]*LF)for k in range(commod))) 
            
### 4 ###
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(grb.quicksum( flights[i,j,k] for j in range(nodes)),
                        GRB.EQUAL,
                        grb.quicksum( flights[j,i,k] for j in range(nodes)))
            
### 5 ###
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(grb.quicksum((grb.quicksum(((distance(i,j)/speed[0][k]+TAT(j,k))*flights[i,j,k])for j in range(nodes)))for i in range(nodes)),
                        GRB.LESS_EQUAL,
                        7*TAT(j,k)*AC[0][k])      


m.update()
m.optimize()

                 
for v in m.getVars():
    print (v.varName, v.x)    
print ('Obj:', m.objVal) 

m.write('MaxProfit.sol')   