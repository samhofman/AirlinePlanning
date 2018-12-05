# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from math import *

from excel_data import *


### AIRPORT ###

nodes = len(airports[0])

# Distances

def dist(i,j):
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
    return;


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
        q = demand[i][j]
     
    return;


def cost_fact(i,j):
    if i == 1 or j == 1:
        c = 0.7
    else:
        c = 1
    
    return;
    
