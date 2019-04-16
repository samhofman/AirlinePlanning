# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 11:56:20 2019

@author: woute
"""

import os,sys
import networkx as nx
import openpyxl as xl
import numpy as np
#import gurobipy as grb
from math import *
#import csv
import decimal
import matplotlib.pyplot as plt

#os.chdir("C:/Users/hofma/Documents/Mijn map/Delft/MSc2/NetworkScheduling/Assignment 1/2. Passengers")

wb = xl.load_workbook("Input.xlsx", read_only=True)
S1 = wb['Flight']
S2 = wb['Itinerary']
S3 = wb['Recapture Rate']

K = 2 #Number of commodities. k=0: economy; k=1: business

### Read Tab 1 ###

arc_no = np.array([[int(i.value) for i in j] for j in S1['A2':'A234']]) #Arc number (integer number!)
flight_no = np.array([[str(i.value) for i in j] for j in S1['B2':'D234']]) #Flight number, origin, destination
flight_time = np.array([[float(i.value) for i in j] for j in S1['E2':'F234']]) #Departure time, ready time
flight_cap = np.array([[float(i.value) for i in j] for j in S1['G2':'H234']]) #Capacity Y, capacity J

### Read Tab 2 ###

itinerary_no = np.array([[int(i.value) for i in j] for j in S2['A2':'A739']]) #Itinerary number (integer number!)
itinerary = np.array([[str(i.value) for i in j] for j in S2['B2':'C739']]) #Origin, destination
demand = np.array([[float(i.value) for i in j] for j in S2['D2':'E739']]) #Demand Y, demand J
fare = np.array([[float(i.value) for i in j] for j in S2['F2':'G739']]) #Fare Y, fare J
leg = np.array([[str(i.value) for i in j] for j in S2['H2':'I739']]) #Flight number leg 1, flight number leg 2
# !!! IF LEG 2 IS EMPTY, FLIGHT NUMBER IS AR0000

### Read Tab 3 ###

recapture_from_to = np.array([[int(i.value) for i in j] for j in S3['A2':'B300']]) #From itinerary, to itinerary (integer numbers!)
r_rate = np.array([[float(i.value) for i in j] for j in S3['C2':'C300']]) #Recapture rate

recapture_from = []
recapture_to = []

for i in range(len(recapture_from_to)):
    recapture_from.append(recapture_from_to[i][0])
    recapture_to.append(recapture_from_to[i][1])







       

