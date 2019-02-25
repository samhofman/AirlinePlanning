# -*- coding: utf-8 -*-
"""
Created on Wed Dec 05 17:16:14 2018

@author: sam
"""
import gurobipy as grb
from math import *
import csv

import sys 
import os
sys.path.append(os.path.abspath("C:\Users\hofma\AirlinePlanning"))


from Functions_P2 import *

GRB = grb.GRB


# CREATE MODEL
m = grb.Model('MaxProfit')


# DECISION VARIABLES
flow     = {}    #x_i,j
hflow    = {}    #w_i,j
flights  = {}    #z_i,j^k
aircraft = {}    #AC^k
aircraft_leased = {}    #m^k
aircraft_sold = {}  #n^k


### CREATE DECISION VARIABLES ###########################################################################################
for i in range(nodes):
    for j in range(nodes):
        flow[i,j] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="x_%s,%s"%(i,j))
        hflow[i,j] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="w_%s,%s"%(i,j))
        
        for k in range(commod):
            flights[i,j,k] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="z_%s,%s_%s"%(i,j,k))
            #aircraft[k] = m.addVar(vtype=GRB.INTEGER, lb=0, #No. of aircraft
            #            name="AC_%s"%(k))
            aircraft_leased[k] = m.addVar(vtype=GRB.INTEGER, lb=0, #No. of extra leased aircraft
                        name="m_%s"%(k)) 
            aircraft_sold[k] = m.addVar(vtype=GRB.INTEGER, lb=0, #No. of extra leased aircraft
                        name="n_%s"%(k)) 
            
m.update()


##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum( y(i,j)*distance(i,j)*(hflow[i,j]+flow[i,j]) -  grb.quicksum((flights[i,j,k]*cost_fact(i,j)*(Cx_ar[0][k]+Ct[0][k]*distance(i,j)/speed[0][k]+Cf[0][k]*F22*distance(i,j)/1.5)) for k in range(commod))for j in range(nodes))for i in range(nodes)) - grb.quicksum((AC[0][k]+aircraft_leased[k]-aircraft_sold[k])*Cl[0][k]+2000.*aircraft_leased[k]+8000.*aircraft_sold[k] for k in range(commod))

m.setObjective(obj,GRB.MAXIMIZE) #fill in obj instead of m.getObjective

print "Objective function created."

##### CONSTRAINTS ########################################################################################################

### 1 ################################################################
# Flow cannot be higher than demand
print "Constraint 1 loading"
for i in range(nodes):
    for j in range(nodes):
        m.addConstr(flow[i,j] + hflow[i,j], GRB.LESS_EQUAL, demand(i,j))

### 2 ################################################################
# Flow transferring at hub cannot be higher than demand
print "Constraint 2 loading"
for i in range(nodes):
    for j in range(nodes):
        m.addConstr(    hflow[i,j], 
                        GRB.LESS_EQUAL, 
                        demand(i,j)*hub(i)*hub(j))

### 3 ################################################################  
# Number of passengers per leg cannot be higher than available seats         
print "Constraint 3 loading"
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(flow[i,j]+grb.quicksum((hflow[i,m]*(1-hub(j)))for m in range(nodes))+grb.quicksum((hflow[m,j]*(1-hub(i)))for m in range(nodes)),
                        GRB.LESS_EQUAL, 
                        grb.quicksum((flights[i,j,k]*seats[0][k]*LF(i,j))for k in range(commod)))           

### 4 ################################################################
# Number of inbound and outbound flights must be equal per aircraft type and per airport
print "Constraint 4 loading"  
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(grb.quicksum( flights[i,j,k] for j in range(nodes)),
                        GRB.EQUAL,
                        grb.quicksum( flights[j,i,k] for j in range(nodes)))           

### 5 ################################################################
# Hours of operation cannot be higher than average utilisation time
print "Constraint 5 loading" 
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(grb.quicksum(grb.quicksum((((distance(i,j)/speed[0][k])+(TAT(j,k)/60.))*flights[i,j,k])for j in range(nodes))for i in range(nodes)),
                        GRB.LESS_EQUAL,
                        7*BT*(AC[0][k]+aircraft_leased[k]-aircraft_sold[k]))      

### 6 ################################################################
# Aircraft of type k cannot fly flight leg if its range is smaller than the distance
print "Constraint 6 loading"
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(flights[i,j,k],
                        GRB.LESS_EQUAL,
                        a(i,j,k))

### 7 ################################################################
# Aircraft type k cannot fly if runway is too short
print "Constraint 7 loading"
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(flights[i,j,k],
                        GRB.LESS_EQUAL,
                        r(i,j,k))
            
### 8 ################################################################
# No intra-EU flights for aircraft types 4 and 5
print "Constraint 8 loading"
for i in range(20):
    for j in range(20):
        for k in range(3,4):
            m.addConstr(grb.quicksum(flights[i,j,k] for j in range(20)),
                        GRB.EQUAL,
                        0.)
            
### 9 ################################################################
# Only US-hub flights are allowed
print "Constraint 9 loading"
for i in range(1,24):
    for j in range(20,24):
        for k in range(commod):
            m.addConstr(grb.quicksum(flights[i,j,k] for j in range(20,24)),
                        GRB.EQUAL,
                        0.)
            
### 10 ################################################################
# Only 7500 seats to/from USA available per week
print "Constraint 10 loading"
m.addConstr(grb.quicksum(grb.quicksum(grb.quicksum((flights[i,j,k]+flights[j,i,k])*seats[0][k] for j in range(20,24)) for k in range(commod)) for i in range(nodes)),
            GRB.LESS_EQUAL,
            7500.) 

### 11 ################################################################
# No more flights than slots available
print "Constraint 11 loading"
for j in range(nodes):         
    m.addConstr(grb.quicksum(grb.quicksum(flights[i,j,k] for k in range(commod)) for i in range(nodes)),
                GRB.LESS_EQUAL,
                slots[j])
    
### 12 ################################################################
# Don't sell more aircraft than available
print "Constraint 12 loading"
for k in range(commod):         
    m.addConstr(aircraft_sold[k],
                GRB.LESS_EQUAL,
                AC[0][k])

m.update()


def mycallback(model, where):
    if where == GRB.Callback.MIP:
        objbnd = model.cbGet(GRB.Callback.MIP_OBJBND)
        objbst = model.cbGet(GRB.Callback.MIP_OBJBST)
        runtime = model.cbGet(GRB.Callback.RUNTIME)
        if runtime > 60:
            print('Stop early - 60s passed')
            model.terminate()
#        elif abs(objbst - objbnd) <= 0.0033 * (abs(objbst)):
#            print('Stop early - 0.33% gap achieved')
#            model.terminate()
            
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
var_w = []
var_z = []
var_m = []
var_n = []


for var in m.getVars():
    # Or use list comprehensions instead 
    if 'x' == str(var.VarName[0]) and var.x > 0:
        var_x.append([var.VarName, var.x])
    if 'w' == str(var.VarName[0]) and var.x > 0:
        var_w.append([var.VarName, var.x])    
    if 'z' == str(var.VarName[0]) and var.x > 0:
        var_z.append([var.VarName, var.x])
    if 'm' == str(var.VarName[0]) and var.x > 0:
        var_m.append([var.VarName, var.x]) 
    if 'n' == str(var.VarName[0]) and var.x > 0:
        var_n.append([var.VarName, var.x]) 
        
# Write to csv
with open('outP2.csv', 'wb') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerows(var_x)
     wr.writerows(var_w)
     wr.writerows(var_z)
     wr.writerows(var_m)
     wr.writerows(var_n)

### Make frequency table for use in P3 ###
f_direct  = np.zeros(shape=(nodes,nodes))

for i in range(nodes):
    for j in range(nodes):
        f_direct[i][j] = grb.LinExpr.getValue(grb.quicksum(flights[i,j,k].x for k in range(commod)))




 

   