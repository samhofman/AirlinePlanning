# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:25:01 2019

@author: woute
"""

from tableaux2 import *
from Functions import *
from initial_solution2 import tableau, pi, sigma, business_cost



### ADD column? ###

def add_col(p,r):
    pi_p = 0.
    pi_r = 0.
    
    for f in range(len(flight_no)):
        for l in range(len(tableau[p][f])-1):
            pi_p = pi_p + tableau[p][f][l]*pi[f]
            pi_r = pi_r + tableau[r][f][l]*pi[f]

    tpr = (path_fare(p, 0) - pi_p) - recap_rate(p, r, 0) * (path_fare(r, 0)-pi_r) - sigma[p]

    return tpr


def tab_add_col(p):
    col = {}
    col[0] = np.zeros((len(flight_no), 1))
    
    for f in range(len(flight_no)):
        col[0][f] = delta(f, p)
    return col[0]
    
    


for p in range(len(itinerary_no)):
    for c in range(len(recapture_from_to)):
        if p == recapture_from_to[c][0]:
            if add_col(p, recapture_from_to[c][1]) < 0. :
                tableau[p] = np.hstack((tableau[p], tab_add_col(p)))
                
                
                
                
                
                