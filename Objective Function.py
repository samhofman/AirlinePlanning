# -*- coding: utf-8 -*-
"""
Created on Wed Dec 05 17:16:14 2018

@author: woute
"""
import gurobipy as grb
from functions import *
from math import *
import csv

GRB = grb.GRB


# CREATE MODEL
m = grb.Model('MaxProfit')


# DECISION VARIABLES
flow     = {}    #x_i,j
hflow    = {}    #w_i,j
flights  = {}    #z_i,j_k
#aircraft = {}    #AC_k



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
            #aircraft[k] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        #name="AC_%s"%(k))

m.update()


##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum( (5.9*dist_fact(i,j)+0.043)*distance(i,j)*(hflow[i,j]+flow[i,j]) -  grb.quicksum((flights[i,j,k]*cost_fact(i,j)*(Cx_ar[0][k]+Ct[0][k]*distance(i,j)/speed[0][k]+Cf[0][k]*F17*distance(i,j)/1.5)) for k in range(commod))for j in range(nodes))for i in range(nodes)) - grb.quicksum(AC[0][k]*Cl[0][k] for k in range(commod))

m.setObjective(obj,GRB.MAXIMIZE) #fill in obj instead of m.getObjective

print "Objective function created."

##### CONSTRAINTS ########################################################################################################

### 1 ################################################################
for i in range(nodes):
    for j in range(nodes):
        m.addConstr(flow[i,j] + hflow[i,j], GRB.LESS_EQUAL, demand(i,j))
print "Constraint 1"
### 2 ################################################################
for i in range(nodes):
    for j in range(nodes):
        m.addConstr(    hflow[i,j], 
                        GRB.LESS_EQUAL, 
                        demand(i,j)*hub(i)*hub(j))
print "Constraint 2"
### 3 ################################################################           
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(flow[i,j]+grb.quicksum((hflow[i,m]*(1-hub(j)))for m in range(nodes))+grb.quicksum((hflow[m,j]*(1-hub(i)))for m in range(nodes)),
                        GRB.LESS_EQUAL, 
                        grb.quicksum((flights[i,j,k]*seats[0][k]*LF)for k in range(commod))) 
print "Constraint 3"            
### 4 ################################################################
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(grb.quicksum( flights[i,j,k] for j in range(nodes)),
                        GRB.EQUAL,
                        grb.quicksum( flights[j,i,k] for j in range(nodes)))
print "Constraint 4"            
### 5 ################################################################
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(grb.quicksum(grb.quicksum((((distance(i,j)/speed[0][k])+(TAT(j,k)/60.))*flights[i,j,k])for j in range(nodes))for i in range(nodes)),
                        GRB.LESS_EQUAL,
                        7*BT*AC[0][k])      
print "Constraint 5"
### 6 ################################################################
for i in range(nodes):
    for j in range(nodes):
        for k in range(commod):
            m.addConstr(flights[i,j,k],
                        GRB.LESS_EQUAL,
                        a(i,j,k))
print "Constraint 6"



m.update()


def mycallback(model, where):
    if where == GRB.Callback.MIP:
        objbnd = model.cbGet(GRB.Callback.MIP_OBJBND)
        objbst = model.cbGet(GRB.Callback.MIP_OBJBST)
        runtime = model.cbGet(GRB.Callback.RUNTIME)
        if runtime > 60:
            model.terminate()
        elif abs(objbst - objbnd) <= 0.0033 * (abs(objbst)):
            print('Stop early - 0.33% gap achieved')
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
var_w = []
var_z = []


for var in m.getVars():
    # Or use list comprehensions instead 
    if 'x' == str(var.VarName[0]) and var.x > 0:
        var_x.append([var.VarName, var.x])
    if 'w' == str(var.VarName[0]) and var.x > 0:
        var_w.append([var.VarName, var.x])    
    if 'z' == str(var.VarName[0]) and var.x > 0:
        var_z.append([var.VarName, var.x])    
# Write to csv
with open('out.csv', 'wb') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerows(var_x)
     wr.writerows(var_w)
     wr.writerows(var_z)




 

   