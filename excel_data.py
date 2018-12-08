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
S3 = wb['AircraftSpecs'] #Tab AircraftSpecs

airport_data = []
airports = []
competition = []
demand = []
demand_hs = []
demand_ls = []
gdp_data = []
pop_city = []


##### READ TAB 1 #####

### POPULATION PER CITY: pop_city ###

pop_city = np.array([[i.value for i in j] for j in S1['B4':'C27']])

#### GDP PER COUNTRY: gdp_data ###

gdp_data = np.array([[i.value for i in j] for j in S1['F4':'G27']])


##### READ TAB 2 #####

### AIRCRAFT ###

AC = np.array([[i.value for i in j] for j in S2['B13':'F13']])

### AIRPORTS ###

airports_eu = np.array([[i.value for i in j] for j in S2['C5':'V5']])
airports    = np.array([[i.value for i in j] for j in S2['C5':'Z5']])

### AIRPORT DATA: airport_data ###

airport_data = np.array([[i.value for i in j] for j in S2['C7':'Z10']])

### DEMAND PER WEEK: demand ###    
 
demand_ar = np.array([[i.value for i in j] for j in S2['C16':'V35']])
    
### DEMAND PER WEEK HIGH SEASON: demand_hs ###    

demand_hs = np.array([[i.value for i in j] for j in S2['C38':'Z61']])
    
### DEMAND PER WEEK LOW SEASON: demand_ls ###       

demand_ls = np.array([[i.value for i in j] for j in S2['C64':'Z87']])

### COMPETITION: competition ###
    
competition = np.array([[i.value for i in j] for j in S2['C90':'Z113']])
    

##### READ TAB 3 #####

### SPEED: speed ###

speed = np.array([[i.value for i in j] for j in S3['B2':'F2']])

### SEATS: seats ###

seats = np.array([[i.value for i in j] for j in S3['B3':'F3']]) 

### TAT: tat ###

tat_ar = np.array([[i.value for i in j] for j in S3['B4':'F4']])

### RANGE: max_range ###

max_range = np.array([[i.value for i in j] for j in S3['B5':'F5']])

### RWY REQ: rwy_req ###

rwy_req = np.array([[i.value for i in j] for j in S3['B6':'F6']])

### LEASE COST: Cl ###

Cl = np.array([[i.value for i in j] for j in S3['B7':'F7']])

### FIXED OPERATING COST: Cx ###

Cx_ar = np.array([[i.value for i in j] for j in S3['B8':'F8']])

### TIME COST PARAMETER: Ct ###

Ct = np.array([[i.value for i in j] for j in S3['B9':'F9']])

### FUEL COST PARAMETER: Cf ###

Cf = np.array([[i.value for i in j] for j in S3['B10':'F10']])




