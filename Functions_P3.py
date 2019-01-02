# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import xlsxwriter
from math import *

from Excel_data_P3 import *
from OF_P2 import f_direct
import csv


### Airports ###

nodes = len(airports[0])

### Aircraft ###

commod = 5              #different aircraft types

### Weeks ###

weeks = 2

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


dist = np.zeros(shape=(24,24))

for i in range(nodes):
    for j in range(nodes):
        dist[i,j] = int(distance(i,j))

#Write distance matrix to excel for problem 2
workbook = xlsxwriter.Workbook('DistancesP2.xlsx')
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

def demand(i,j,w):
    if w == 0:
        q = demand_hs[i][j]*MS(i,j)
    elif w == 1:
        q = demand_ls[i][j]*MS(i,j)
    else:
        print "Error: more than 2 weeks."
        exit()
     
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

def LF(i,j):
    if 20 <= i <= 23 or 20 <= j <= 23: #Load factor for flights to/from USA
        LF = 0.85
    else: #Load factor intra-European flights
        LF = 0.75
    return LF;

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
        ax = 10000 #Possible to fly
    else:
        ax = 0 #Impossible to fly
    
    return ax;

### RWY length limit factor ###
    
def r(i,j,k):
    if rwy_length[i] >= rwy_req[0][k] and rwy_length[j] >= rwy_req[0][k]:
        rx = 10000 #Possible to fly
    else:
        rx = 0 #Imossible to fly
    return rx;

### Yield function ###

def y(i,j):
    if 20 <= i <= 23 or 20 <= j <= 23: #For flights to/from USA
        y_ij = 0.05 
    else: #For intra-European flights
        y_ij = 5.9*dist_fact(i,j)+0.043
    return y_ij;

### Frequency functions ###

def freq_direct(i,j):
    freq = f_direct[i][j]
    return freq;

def freq_indirect(i,j):
    freq = min(freq_direct(i,0),freq_direct(0,j))
    return freq;

### Market share function ###

def MS(i,j):
    a = 1.0
    b = 1.7
    if freq_direct(i,j) + freq_indirect(i,j) > 0: #We already have route
        MS = ((freq_direct(i,j)**a)+(freq_indirect(i,j)**b))/((freq_direct(i,j)**a)+(freq_indirect(i,j)**b)+(competition[i,j]**a))
    elif freq_direct(i,j) + freq_indirect(i,j) == 0: #We don't fly the route
        if competition[i,j] > 0: #Competition already flies the route
            MS = 0.
        else: #Competition doesn't fly the route
            MS = 1.
    return MS;

### Create demand for first iteration ###
initial_demand_week1 = np.zeros(shape=(24,24))
initial_demand_week2 = np.zeros(shape=(24,24))

for i in range(nodes):
    for j in range(nodes):
        w = 0
        initial_demand_week1[i,j] = int(demand(i,j,w))
        

for i in range(nodes):
    for j in range(nodes):
        w = 1
        initial_demand_week2[i,j] = int(demand(i,j,w))

### Write demand matrix to csv for problem 3 ###


with open('Initial_Demand_P3_0.csv', 'wb') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerows(initial_demand_week1)

with open('Initial_Demand_P3_1.csv', 'wb') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerows(initial_demand_week2)
    