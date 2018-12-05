# -*- coding: utf-8 -*-
"""
Created on Wed Dec 05 17:16:14 2018

@author: woute
"""
import gurobipy as grb
from functions import *

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

# obj = sum ...
m.setObjective(m.getObjective(),GRB.MAXIMIZE)#fill in obj instead of m.getObjective





            
            

                 
    
    