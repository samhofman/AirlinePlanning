# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import xlsxwriter
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
    
    a = sin(dlat / 2.)**2 + cos(lat_i) * cos(lat_j) * sin(dlon / 2.)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    d = R * c
    return d;


dist = np.zeros(shape=(20,20))

for i in range(nodes):
    for j in range(nodes):
        dist[i,j] = int(distance(i,j))

#Write distance matrix to excel for problem 2
workbook = xlsxwriter.Workbook('Distances.xlsx')
worksheet = workbook.add_worksheet()

array = dist

row = 0

for col, data in enumerate(array):
    worksheet.write_column(row, col, data)

workbook.close()

#d_i,j ** -0.76: distance cannot be 0 -> create function dist_fact(i,j)

def dist_fact(i,j):
    if i == j:
        di = 0
    else:
        di = distance(i,j)**(-0.76)
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

### Cost factor ###

def cost_fact(i,j):
    if i == 0 or j == 0:
        c = 0.7
    else:
        c = 1
    
    return c;

### Hub factor ###
   
def hub(h):
    if h == 0:
        g = 0
    else:
        g = 1
    
    return g;

### Load Factor ###

LF = 0.75

### Turn-around time ###

def TAT(j,k):
    if j == 0:
        tat = max(2*tat_ar[0][k],60)
    else:
        tat = tat_ar[0][k]
        
    return tat;

### Range limit factor ###

def a(i,j,k):
    if distance(i,j) <= max_range[0][k]:
        ax = 10000
    else:
        ax = 0
    
    return ax;
    


