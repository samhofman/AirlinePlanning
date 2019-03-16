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


### Read Tab 1 ###

flight_no = np.array([[str(i.value) for i in j] for j in S1['A2':'C233']])
flight_time = np.array([[float(i.value) for i in j] for j in S1['D2':'E233']])
flight_cap = np.array([[float(i.value) for i in j] for j in S1['F2':'G233']])

### Read Tab 2 ###

itinerary_no = np.array([[float(i.value) for i in j] for j in S2['A2':'A738']])
itinerary = np.array([[str(i.value) for i in j] for j in S2['B2':'C738']])
demand = np.array([[float(i.value) for i in j] for j in S2['D2':'E738']])
fare = np.array([[float(i.value) for i in j] for j in S2['F2':'G738']])
leg = np.array([[str(i.value) for i in j] for j in S2['H2':'I738']])

### Read Tab 3 ###

recapture = np.array([[float(i.value) for i in j] for j in S3['A2':'C300']])




        
        

