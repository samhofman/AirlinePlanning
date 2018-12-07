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
aircraft = {}    #AC_k



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
            aircraft[k] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="AC_%s"%(k))

m.update()


#d_i,j ** -0.76: distance cannot be 0 -> create function dist_fact(i,j)

def dist_fact(i,j):
    if i == j:
        di = 0
    else:
        di = distance(i,j)
    return di;

obj = grb.quicksum(grb.quicksum( (5.9*dist_fact(i,j)+0.043)*distance(i,j)*(hflow[i,j]+flow[i,j]) -  grb.quicksum((Cl[0][k]+cost_fact(i,j)*(Cx[0][k]+Ct[0][k]*distance(i,j)/speed[0][k]+Cf[0][k]*flights[i,j,k]*distance(i,j)/1.5)) for k in range(commod))for j in range(nodes))for i in range(nodes))



m.setObjective(obj,GRB.MAXIMIZE) #fill in obj instead of m.getObjective





            
            

                 
    
    