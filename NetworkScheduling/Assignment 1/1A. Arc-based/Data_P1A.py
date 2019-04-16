# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:46:21 2019

@author: woute
"""

import openpyxl as xl
import numpy as np

wb = xl.load_workbook("Input_Ass1P1.xlsx", read_only=True)
S1 = wb['Arcs'] #Tab arcs
S2 = wb['Commodities'] #Tab commodities

### Read Tab 1 ###

arcs = np.array([[i.value for i in j] for j in S1['A2':'E31']])

### Read Tab 2 ###

commodities = np.array([[i.value for i in j] for j in S2['A2':'D41']])

