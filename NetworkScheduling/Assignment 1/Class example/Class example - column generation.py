# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 11:56:20 2019

@author: woute
"""

import networkx as nx
import openpyxl as xl
import numpy as np
#import gurobipy as grb
from math import *
import csv
import matplotlib.pyplot as plt


wb = xl.load_workbook("Class_example_data.xlsx", read_only=True)
S1 = wb['Sheet1']

### Read Tab 1 ###

arcs = np.array([[i.value for i in j] for j in S1['A2':'E8']])

### Read Tab 2 ###

commodities = np.array([[i.value for i in j] for j in S1['A12':'D15']])



### Calculate shortest path for each commodity ###

G = nx.DiGraph()

for i in range(len(arcs)):
    G.add_edge(arcs[i][1], arcs[i][2], weight = arcs[i][3])
 

# Implement arcs and weights

P = []        #Set with all paths per commodity

for i in range(len(commodities)):
    P.append([p for p in nx.all_simple_paths(G, source = commodities[i][1], target = commodities[i][2] )])
    

delta = {}    
for k in range(len(commodities)):
    delta[k] = np.zeros((len(arcs),len(P[k])))
    
for k in range(len(commodities)):
    for n in range(len(P[k])):
        for a in range(len(arcs)):
                for i in range(len(P[k][n])-1):
                    if P[k][n][i] == arcs[a][1] and P[k][n][i+1] == arcs[a][2]:
                        delta[k][a][n] = 1
            
            

        
        
        
        

