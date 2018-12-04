# -*- coding: utf-8 -*-
"""
Created on Tue Dec 04 09:34:11 2018

@author: woute
"""

import openpyxl as xl
import numpy as np


wb = xl.load_workbook("Datasheet.xlsx", read_only=True)

S1 = wb['General'] #Tab General
S2 = wb['Group 6'] #Tab Group 6


##### READ TAB 1 #####

### POPULATION PER CITY: pop_city ###

pop_city = np.array([[i.value for i in j] for j in S1['B4':'C27']])

#### GDP PER COUNTRY: gdp_data ###

gdp_data = np.array([[i.value for i in j] for j in S1['F4':'G27']])


##### READ TAB 2 #####

### AIRPORT DATA: airport_data ###

airport_data = np.array([[i.value for i in j] for j in S2['C7':'Z10']])

### DEMAND PER WEEK: demand ###    
 
demand = np.array([[i.value for i in j] for j in S2['C16':'V35']])
    
### DEMAND PER WEEK HIGH SEASON: demand_hs ###    

demand_hs = np.array([[i.value for i in j] for j in S2['C38':'Z61']])
    
### DEMAND PER WEEK LOW SEASON: demand_ls ###       

demand_ls = np.array([[i.value for i in j] for j in S2['C64':'Z87']])

### COMPETITION: competition ###
    
competition = np.array([[i.value for i in j] for j in S2['C90':'Z113']])
    