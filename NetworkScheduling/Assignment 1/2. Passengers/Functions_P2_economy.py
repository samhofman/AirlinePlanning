# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 13:09:39 2019

@author: hofma
"""

from tableaux_P2_economy import *

#Note: k=0: economy; k=1: business

#Determine fare per itinerary (=path)
def path_fare(p,k):
    if k == 0: #For economy
        path_fare = fare[p][k] 
    elif k == 1: #For business
        path_fare = fare[p][k]
    return path_fare
    
#Determine recapture rate
def recap_rate(p,r,k):
    if k == 0: #For economy
        for n in range(len(recapture_from_to)):
            if recapture_from_to[n][0] == p and recapture_from_to[n][1] == r:
                recap_rate = r_rate[n][0]
                break
            else: #If reallocation from p to r does not exist, all pax are spilled
                recap_rate = 0.
    elif k == 1: #For business the recapture rate is zero
        recap_rate = 0.
    return recap_rate

#Determine flight capacity
def CAP(f,k):
    if k == 0:
        flight_capacity = flight_cap[f][0]
    elif k == 1:
        flight_capacity = flight_cap[f][1]
    else:
        flight_capacity = 0.
    return flight_capacity

#Determine if flight is in itinerary (=path)
def delta(f,p):
    flight_number = flight_no[f][0]
    itinerary_number = itinerary_no[p][0]
    if flight_number == leg[itinerary_number][0] or flight_number == leg[itinerary_number][1]:
        delta = 1.
    else:
        delta = 0.
    return delta

#Determine daily unconstrained demand per itinerary (=path)
def D(p,k):
    if k == 0:
        unconstr_demand_path = demand[p][0]
    elif k == 1:
        unconstr_demand_path = demand[p][1]
    else:
        unconstr_demand_path = 0.
    return unconstr_demand_path

#Determine daily unconstrained demand on flight leg
def Q(f,k):
    unconstr_demand_flight = 0.
    for p in range(len(itinerary_no)):
        unconstr_demand_flight = unconstr_demand_flight + (delta(f,p)*D(p,k))
    return unconstr_demand_flight

#Determine function needed for initial column generation
def Q_CAP(f,k):
    RHS = Q(f,k)-CAP(f,k)
    return RHS