# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:29:33 2019

@author: hofma
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
S1 = wb['B737']

### Read S1 (B737) ###

arc_no_737 = np.array([[int(i.value) for i in j] for j in S1['A2':'A101']]) #Arc number (integer number!)
flight_no_737 = np.array([[str(i.value) for i in j] for j in S1['B2':'D101']]) #Flight number, origin, destination
flight_time_737 = np.array([[float(i.value) for i in j] for j in S1['E2':'F101']]) #Departure time, arrival time in minutes past midnight
flight_cost_737 = np.array([[float(i.value) for i in j] for j in S1['G2':'J101']]) #Operating cost A330, A340, B737, B738

