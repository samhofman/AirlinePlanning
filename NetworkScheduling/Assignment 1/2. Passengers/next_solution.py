# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:25:01 2019

@author: woute
"""

from tableaux2 import *
from Functions import *
from initial_solution2 import tableau, pi, sigma



### ADD column? ###

def add_col(p,r):
    pi_i = 0.
    pi_j = 0.
    
    for f in range(len(flight_no)):
        pi_i = pi_i + delta(f, p) * pi[f]
        pi_j = pi_j + delta(f, r) * pi[f]
        
    tpr = (path_fare(p,0)-pi_i) - recap_rate(p, r, 0) * (path_fare(r, k) - pi_j) - sigma[p]

    return tpr

def tab_add_col(p):
    col = {}
    col[0] = np.zeros((len(flight_no), 1))
    
    for f in range(len(flight_no)):
        col[0][f] = delta(f, p)
    return col[0]
    
    

#
#for p in range(len(itinerary_no)):
#    for c in range(len(recapture_from_to)):
#        if p == recapture_from_to[c][0]:
#            if add_col(p, recapture_from_to[c][1]) < 0. :
#                tableau[p] = np.hstack((tableau[p], tab_add_col(p)))
                
                
                
                
                
                