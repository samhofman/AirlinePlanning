# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 14:46:21 2019

@author: woute
"""

import xlrd
import numpy as np

wb = xlrd.open_workbook("Input_Ass1P1.xlsx")
S1 = wb.sheet_by_index(0)
S2 = wb.sheet_by_index(1)


Arcs = []   #From, To, Cost


for i in range(1,31):
    arc = (str(S1.cell_value(i,1)), str(S1.cell_value(i,2)), S1.cell_value(i,3))
    Arcs.append(arc)    
