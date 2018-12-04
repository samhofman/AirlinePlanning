# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from math import *

from excel_data import *



### AIRPORT DISTANCES ###

def d(i,j):
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
low_season = True
high_season = True

if low_season == True and high_season == True:
    print "low or high season?"    


def q(i,j):
    if low_season == True:
        q = demand_ls[i][j]
    elif high_season == True:
        q = demand_hs[i][j]
    else:
        q = demand[i][j]
    
    print q    
    return;



