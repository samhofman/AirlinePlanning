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


wb = xl.load_workbook("Input_Ass1P1.xlsx", read_only=True)
S1 = wb['Arcs']
S2 = wb['Commodities']

### Read Tab 1 ###

arcs = np.array([[i.value for i in j] for j in S1['A2':'E31']])

### Read Tab 2 ###

commodities = np.array([[i.value for i in j] for j in S2['A2':'D41']])


### COST ###

cost = np.zeros((len(arcs),len(arcs)))

for i in range(len(arcs)):
        a = arcs[i,1]
        b = arcs[i,2]
        cost[a,b] = arcs[i,3]
        cost[b,a] = arcs[i,3]

capacity = np.zeros((len(arcs),len(arcs)))

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


#nx.draw(G)
#plt.show()


# Implement arcs and weights
SP = []
P = []        #P[k][p][n] k commodity, p path number, n node

for i in range(len(commodities)):
    SP.append([p for p in nx.shortest_path(G, source = commodities[i][1], target = commodities[i][2] )])
    P.append([p for p in nx.all_simple_paths(G, source = commodities[i][1], target = commodities[i][2] )])
    
###TABLEAU
#delta_arc = {}  #delta[k][a][p]  
#for k in range(len(commodities)):
#    delta_arc[k] = np.zeros((len(arcs),len(P[k])))
#
#   
#for k in range(len(commodities)):
#    for p in range(len(P[k])):
#        for a in range(len(arcs)):
#                for n in range(len(P[k][p])-1):
#                    if P[k][p][n] == arcs[a][1] and P[k][p][n+1] == arcs[a][2]:
#                        delta_arc[k][a][p] = 1.
#                    elif P[k][p][n] == arcs[a][2] and P[k][p][n+1] == arcs[a][1]:
#                        delta_arc[k][a][p] = 1.
            
#Shortest paths
delta_sp= {}    #delta[k][a][p]    
for k in range(len(commodities)):
    delta_sp[k] = np.zeros((len(arcs),1))


for k in range(len(commodities)):
    for a in range(len(arcs)):
        p = 0
        for n in range(len(SP[k])-1):
            if SP[k][n] == arcs[a][1] and SP[k][n+1] == arcs[a][2]:
                delta_sp[k][a][p] = 1.
            elif SP[k][n] == arcs[a][2] and SP[k][n+1] == arcs[a][1]:
                delta_sp[k][a][p] = 1.            
        


def delta(k,p,i):
    delta = delta_sp[k][i][p]
    return delta
    
       
def c(a):
    c = arcs[a][3] 
    return c

def u(v):
    u = arcs[v][4]
    return u

def d(k):
    d = quantity[k]
    return d

def cp(k,p):
    cp = 0.
    for a in range(len(arcs)):
        cp = cp + delta_sp[k][a][p] * arcs[a][3]
    return cp 

        
        

