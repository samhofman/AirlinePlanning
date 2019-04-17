# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 11:56:20 2019

@author: woute
"""

import os,sys
import networkx as nx
import openpyxl as xl
import numpy as np
from math import *
import decimal
import matplotlib.pyplot as plt

#os.chdir("C:/Users/hofma/Documents/Mijn map/Delft/MSc2/NetworkScheduling/Assignment 1/2. Passengers")

wb = xl.load_workbook("Assignment2.xlsx", read_only=True)
S1 = wb['Flight']
S2 = wb['Bus']
S3 = wb['Itinerary']
S4 = wb['Recapture Rate']
S5 = wb['Aircraft']



### Read Tab 1 ###

arc_no = np.array([[int(i.value) for i in j] for j in S1['A2':'A210']]) #Arc number (integer number!)
flight_no = np.array([[str(i.value) for i in j] for j in S1['B2':'D210']]) #Flight number, origin, destination
flight_time = np.array([[float(i.value) for i in j] for j in S1['E2':'F210']]) #Departure time, arrival time in minutes past midnight
flight_cost = np.array([[float(i.value) for i in j] for j in S1['G2':'J210']]) #Operating cost A330, A340, B737, B738


#Create list of unique airports
origin = np.array([[str(i.value) for i in j] for j in S1['C2':'C210']]) #List of origin airports
destination = np.array([[str(i.value) for i in j] for j in S1['D2':'D210']]) #List of destination airports
airports = []
for i in range(len(origin)):
    airports.append(origin[i][0]) #add all airports (origin from flights)
    airports.append(destination[i][0])
airports = list(set(airports)) #remove duplicates
airports.sort()
airports.remove('HALLO')
airports.remove('METGERT')
### Read Tab 2 ###

arc_no_bus = np.array([[int(i.value) for i in j] for j in S2['A2':'A25']]) #Arc number (integer number!)
flight_no_bus = np.array([[str(i.value) for i in j] for j in S2['B2':'D25']]) #Flight number, origin, destination
flight_time_bus = np.array([[float(i.value) for i in j] for j in S2['E2':'F25']]) #Departure time, arrival time in minutes past midnight
flight_cost_bus = 4500. #Operating cost for flights by bus

### Read Tab 3 ###

itinerary_no = np.array([[int(i.value) for i in j] for j in S3['A2':'A773']]) #Itinerary number (integer number!)
itinerary = np.array([[str(i.value) for i in j] for j in S3['B2':'C773']]) #Origin, destination
demand = np.array([[float(i.value) for i in j] for j in S3['D2':'E773']]) #Demand Y, demand J
fare = np.array([[float(i.value) for i in j] for j in S3['F2':'G773']]) #Fare Y, fare J
leg = np.array([[str(i.value) for i in j] for j in S3['H2':'I773']]) #Flight number leg 1, flight number leg 2
# !!! IF LEG 2 IS EMPTY, FLIGHT NUMBER IS AR0000

### Read Tab 4 ###

recapture_from_to = np.array([[int(i.value) for i in j] for j in S4['A2':'B6107']]) #From itinerary, to itinerary (integer numbers!)
r_rate = np.array([[float(i.value) for i in j] for j in S4['C2':'C6107']]) #Recapture rate

recapture_from = []
recapture_to = []

for i in range(len(recapture_from_to)):
    recapture_from.append(recapture_from_to[i][0])
    recapture_to.append(recapture_from_to[i][1])

### Read Tab 5 ###

k_units = np.array([[float(i.value) for i in j] for j in S5['C2':'C5']]) #Number of units for each fleet type k
seats = np.array([[float(i.value) for i in j] for j in S5['D2':'E5']]) #Number of seats for each fleet type k (economy, business)
TAT = np.array([[float(i.value) for i in j] for j in S5['F2':'F5']]) #TAT for each fleet type k


       

