# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:09:28 2019

@author: hofma
"""

from Data import *

### Make cost matrix ###

cost = np.zeros(shape=(16,16))

for i in range(len(arcs)):
        a = arcs[i,1]
        b = arcs[i,2]
        cost[a,b] = arcs[i,3]
        
### Make capacity matrix ###

capacity = np.zeros(shape=(16,16))

for i in range(len(arcs)):
        a = arcs[i,1]
        b = arcs[i,2]
        capacity[a,b] = arcs[i,4]

### Make quantity matrix ###

quantity = np.zeros(shape=(16,16))

for i in range(len(commodities)):
    a = commodities[i,1]
    b = commodities[i,2]
    capacity[a,b] = commodities[i,3]
    
### Demand function ###

def d(i,k):
    if i == commodities[k,1]:
        d = float(commodities[k,3])
    elif i == commodities[k,2]:
        d = -float(commodities[k,3])
    else:
        d = 0.0
    return d