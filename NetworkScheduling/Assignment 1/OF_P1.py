# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 16:49:08 2019

@author: hofma
"""

import gurobipy as grb
from math import *
import csv

from Functions_P1 import *

GRB = grb.GRB

# CREATE MODEL
m = grb.Model('MaxProfit')


# DECISION VARIABLES
flow     = {}    #x_i,j_k

### CREATE DECISION VARIABLES ###########################################################################################
for i in range(len(arcs)):
    for j in range(len(arcs)):
        for k in range(len(commodities)):
            flow[i,j,k] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="x_%s,%s_%s"%(i,j,k))


m.update()

##### OBJECTIVE FUNCTION #################################################################################################

obj = grb.quicksum(grb.quicksum( ))

m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective

print "Objective function created."