# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 11:56:20 2019

@author: woute
"""

import networkx as nx
import openpyxl as xl
import numpy as np
import gurobipy as grb
from math import *
import csv

wb = xl.load_workbook("Input_Ass1P1.xlsx", read_only=True)
S1 = wb['Arcs'] #Tab arcs
S2 = wb['Commodities'] #Tab commodities

### Read Tab 1 ###

arcs = np.array([[i.value for i in j] for j in S1['A2':'E31']])

### Read Tab 2 ###

commodities = np.array([[i.value for i in j] for j in S2['A2':'D41']])



### Calculate shortest path for each commodity ###

G = nx.Graph()

# Implement arcs and weights
for i in range(len(arcs)):
    G.add_edge(arcs[i][1], arcs[i][2], weight = arcs[i][3])


SP_init = []    #list of shortest path for each commodity
P = []        #Set with all paths per commodity
for i in range(len(commodities)):
    SP_init.append(nx.shortest_path(G, source = commodities[i][1], target = commodities[i][2]))
    
    P.append([p for p in nx.all_simple_paths(G, source = commodities[i][1], target = commodities[i][2] )])




GRB = grb.GRB

# CREATE MODEL
m = grb.Model('MaxProfit-Column')


# DECISION VARIABLES
fraction    = {}    #f_k,p

for k in range(len(commodities)):
    for p in range(len(P[k])):
        fraction[k,p] = m.addVar(vtype=GRB.INTEGER, lb=0,
                        name="f_%s,%s"%(k,p))

m.update()

