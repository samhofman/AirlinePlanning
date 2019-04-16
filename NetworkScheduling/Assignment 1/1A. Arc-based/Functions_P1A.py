# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 15:09:28 2019

@author: hofma
"""

import xlsxwriter
from Data_P1A import *

### Make cost matrix ###

cost = np.zeros(shape=(16,16))

for i in range(len(arcs)):
        a = arcs[i,1]
        b = arcs[i,2]
        cost[a,b] = arcs[i,3]
        
cost = np.maximum( cost, cost.transpose() ) #Make matrix symmetric to work in both directions

workbook = xlsxwriter.Workbook('Cost_P1.xlsx') #Write to Excel to check
worksheet = workbook.add_worksheet('Cost')

array = cost

row = 0

for col, data in enumerate(array):
    worksheet.write_column(row, col, data)

workbook.close()

### Determine number of airports ###

airports = len(cost)
        
### Make capacity matrix ###

capacity = np.zeros(shape=(16,16))

for i in range(len(arcs)):
        a = arcs[i,1]
        b = arcs[i,2]
        capacity[a,b] = arcs[i,4]
        
capacity = np.maximum( capacity, capacity.transpose() ) #Make matrix symmetric to work in both directions

workbook = xlsxwriter.Workbook('Capacity_P1.xlsx') #Write to Excel to check
worksheet = workbook.add_worksheet('Capacity')

array = capacity

row = 0

for col, data in enumerate(array):
    worksheet.write_column(row, col, data)

workbook.close()

### Make quantity matrix ###

quantity = np.zeros(shape=(16,16))

for i in range(len(commodities)):
    a = commodities[i,1]
    b = commodities[i,2]
    quantity[a,b] = commodities[i,3]
    
workbook = xlsxwriter.Workbook('Quantity_P1.xlsx') #Write to Excel to check
worksheet = workbook.add_worksheet('Capacity')

array = quantity

row = 0

for col, data in enumerate(array):
    worksheet.write_column(row, col, data)

workbook.close()
    
### Demand function ###

def d(i,k):
    if i == commodities[k,1]:
        d = float(commodities[k,3])
    elif i == commodities[k,2]:
        d = -float(commodities[k,3])
    else:
        d = 0.0
    return d

### Cost function ###

def c(i,j):
    c = cost[i,j]
    return c

### Capacity function ###

def u(i,j):
    u = capacity[i,j]
    return u
    