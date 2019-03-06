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
#import csv
import matplotlib.pyplot as plt


wb = xl.load_workbook("Class_example_data.xlsx", read_only=True)
S1 = wb['Sheet1']

### Read Tab 1 ###

arcs = np.array([[i.value for i in j] for j in S1['A2':'E8']])

### Read Tab 2 ###

commodities = np.array([[i.value for i in j] for j in S1['A12':'D15']])


### COST ###

cost = np.zeros((7,7))

for i in range(len(arcs)):
        a = arcs[i,1]
        b = arcs[i,2]
        cost[a,b] = arcs[i,3]
        cost[b,a] = arcs[i,3]

capacity = np.zeros((7,7))

for i in range(len(arcs)):
        a = arcs[i,1]
        b = arcs[i,2]
        capacity[a,b] = arcs[i,4]
        capacity[b,a] = arcs[i,4]

quantity = commodities[:,3]


### Calculate shortest path for each commodity ###

G = nx.Graph()

for i in range(len(arcs)):
    G.add_edge(arcs[i][1], arcs[i][2], weight = arcs[i][3])
 




# Implement arcs and weights

P = []        #P[k][e][n] k commodity, p path number, n node

for i in range(len(commodities)):
    P.append([p for p in nx.all_simple_paths(G, source = commodities[i][1], target = commodities[i][2] )])
    

delta_arc = {}  #delta[k][a][e]  
for k in range(len(commodities)):
    delta_arc[k] = np.zeros((len(arcs),len(P[k])))
    
for k in range(len(commodities)):
    for p in range(len(P[k])):
        for a in range(len(arcs)):
                for n in range(len(P[k][p])-1):
                    if P[k][p][n] == arcs[a][1] and P[k][p][n+1] == arcs[a][2]:
                        delta_arc[k][a][p] = 1
            
            
def delta(k,p,i,j):
    for a in range(len(arcs)):
        if i == arcs[a][1] and j == arcs[a][2]:
            delta = delta_arc[k][a][p]
    return delta
    
       
def c(i,j):
    c = cost[i][j] 
    return c

def u(v):
    u = arcs[v][4]
    return u

def d(k):
    d = quantity[k]
    return d

def cp(k,p):
    cp = 0
    for a in range(len(arcs)):
        cp = cp + delta_arc[k][a][p] * arcs[a][3]
    return cp 

        
        

