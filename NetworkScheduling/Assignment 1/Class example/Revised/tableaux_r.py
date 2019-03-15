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


arcs = np.array([[i.value for i in j] for j in S1['A2':'E8']])
commodities = np.array([[i.value for i in j] for j in S1['A12':'D15']])


### COST ###

cost = np.zeros((len(arcs),len(arcs)))

for i in range(len(arcs)):
        a = arcs[i,1]
        b = arcs[i,2]
        cost[a,b] = arcs[i,3]
        
capacity = np.zeros((len(arcs),len(arcs)))


for i in range(len(arcs)):
        a = arcs[i,1]
        b = arcs[i,2]
        capacity[a,b] = arcs[i,4]

quantity = commodities[:,3]


### Calculate shortest path for each commodity ###

G = nx.DiGraph()

for i in range(len(arcs)):
    G.add_edge(arcs[i][1], arcs[i][2], weight = arcs[i][3])



# Implement arcs and weights
SP = []


for i in range(len(commodities)):
    SP.append([[p for p in nx.dijkstra_path(G, source = commodities[i][1], target = commodities[i][2] )]])


         
### Shortest paths 1 and 0's ###
    
delta_sp= {}    #delta[k][a][p]    
for k in range(len(commodities)):
    delta_sp[k] = np.zeros((len(arcs),1))


for k in range(len(commodities)):
    for a in range(len(arcs)):
        for p in range(len(SP[k])):
            for n in range(len(SP[k][p])-1):
                if SP[k][p][n] == arcs[a][1] and SP[k][p][n+1] == arcs[a][2]:
                    delta_sp[k][a][p] = 1.
                elif SP[k][p][n] == arcs[a][2] and SP[k][p][n+1] == arcs[a][1]:
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

def sl(a):
    slack = 0.
    for k in range(len(commodities)):
        for p in range(len(SP[k])):
            slack = slack + delta_sp[k][a][p]*d(k)
    
    if slack > u(a):
        sl = 1.
    
    else:
        sl = 0.
    return sl  
            
                     

    
   
        
        

