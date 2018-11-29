# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import xlrd as xl

wb = xl.open_workbook('Datasheet.xlsx')

S1 = wb.sheet_by_index(0) #Tab General
S2 = wb.sheet_by_index(1) #Tab Group 6


##### READ TAB 1 #####

### POPULATION PER CITY: pop_city ###

pop_city=[]
for row in range(3,27):
    _row = []
    for col in range(1,3):
        _row.append(S1.cell_value(row,col))
    pop_city.append(_row)

### GDP PER COUNTRY: gdp_data ###
    
gdp_data=[]
for row in range(3,27):
    _row = []
    for col in range(5,7):
        _row.append(S1.cell_value(row,col))
    gdp_data.append(_row)    



###### READ TAB 2 #####

### AIRPORT DATA: airport_data ###

airport_data=[]
for row in range(6,10):
    _row = []
    for col in range(2,26):
        _row.append(S2.cell_value(row,col))
    airport_data.append(_row)
    
### DEMAND PER WEEK: demand_pw ###    
 
demand_pw=[]
for row in range(15,35):
    _row = []
    for col in range(2,22):
        _row.append(S2.cell_value(row,col))
    demand_pw.append(_row)
    
### DEMAND PER WEEK HIGH SEASON: demand_hs ###    

demand_hs=[]
for row in range(37,61):
    _row = []
    for col in range(2,26):
        _row.append(S2.cell_value(row,col))
    demand_hs.append(_row)
    
### DEMAND PER WEEK LOW SEASON: demand_ls ###       

demand_ls=[]
for row in range(63,87):
    _row = []
    for col in range(2,26):
        _row.append(S2.cell_value(row,col))
    demand_ls.append(_row)

### COMPETITION: competition ###
    
competition=[]
for row in range(89,113):
    _row = []
    for col in range(2,26):
        _row.append(S2.cell_value(row,col))
    competition.append(_row)