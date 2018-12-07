# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from math import *

from excel_data import *


### AIRPORT ###

nodes = len(airports_eu[0])

# Aircraft

commod = 3              #different aircraft

# Distances

def distance(i,j):
    R = 6373.0
    
    lat_i = radians(airport_data[0][i])
    lat_j = radians(airport_data[0][j])
    lon_i = radians(airport_data[1][i])
    lon_j = radians(airport_data[1][j])
    
    dlon = lon_j - lon_i
    dlat = lat_j - lat_i
    
    a = sin(dlat / 2)**2 + cos(lat_i) * cos(lat_j) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    d = R * c
    return d;


dist = np.zeros(shape=(24,24))

for i in range(nodes):
    for j in range(nodes):
        dist[i,j] = int(distance(i,j))   

#d_i,j ** -0.76: distance cannot be 0 -> create function dist_fact(i,j)

def dist_fact(i,j):
    if i == j:
        di = 0
    else:
        di = distance(i,j)
    return di;   

### DEMAND ###
low_season = False
high_season = False

if low_season == True and high_season == True:
    print "low or high season?"  
    exit()


def demand(i,j):
    if low_season == True:
        q = demand_ls[i][j]
    elif high_season == True:
        q = demand_hs[i][j]
    else:
        q = demand_ar[i][j]
     
    return q;


def cost_fact(i,j):
    if i == 1 or j == 1:
        c = 0.7
    else:
        c = 1
    
    return c;
   
def hub(h):
    if h == 0:
        g = 0
    else:
        g = 1
    
    return g;

### Load Factor ###

LF = 0.75

def TAT(j,k):
    if j == 1:
        tat = max(2*tat_ar[0][k],60)
    else:
        tat = tat_ar[0][k]
        
    return tat;

def CX(i,j,k):
    if distance(i,j) <= max_range[0][k]:
        Cx = 1000000
    else:
        Cx = Cx_ar[0][k]
    
    return Cx;
    


