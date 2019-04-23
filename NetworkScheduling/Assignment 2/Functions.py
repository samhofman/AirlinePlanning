# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 12:21:11 2019

@author: hofma
"""

from Input import *
from Time_Space import *

#Make function to get cost of operating flight i with a/c type k
def costki(k,i):
    row_no = 0
    cost = 0
    for j in arc_no:
        if i == j:
            cost = flight_cost[row_no,k]
        row_no += 1
    return cost

#Make function to get economy fare for itinerary p
def fare_e(p):
    fare_e = fare[p,0]
    return fare_e

#Make function to get business fare for itinerary p
def fare_b(p):
    fare_b = fare[p,1]
    return fare_b

#Make function to get recapture rate
def b_p_r(p,r):
    for n in range(len(recapture_from_to)):
        if recapture_from_to[n][0] == p and recapture_from_to[n][1] == r:
            recap_rate = r_rate[n][0]
            break
        else: #If reallocation from p to r does not exist, all pax are spilled
                recap_rate = 0.
    return recap_rate

#Make function to get number of aircraft type k
def AC_k(k):
    AC_k = k_units[k,0]
    return AC_k

#Make function to get seat capacity for economy
def s_k_e(k):
    seats_k = seats[k,0]
    return seats_k

#Make function to get seat capacity for business
def s_k_b(k):
    seats_k = seats[k,1]
    return seats_k

#Make function to get if flight i is in path p
def delta_i_p(i,p):
    flight_number = flight_no_allflights[i][0]
    itinerary_number = itinerary_no[p][0]
    if flight_number == leg[itinerary_number][0] or flight_number == leg[itinerary_number][1]:
        delta = 1.
    else:
        delta = 0.
    return delta

#Determine daily unconstrained economy demand per path
def D_p_e(p):
    unconstr_demand_path = demand[p][0]
    return unconstr_demand_path

#Determine daily unconstrained business demand per path
def D_p_b(p):
    unconstr_demand_path = demand[p][1]
    return unconstr_demand_path

#Make function to get unconstrained economy demand for flight i
def Q_i_e(i):
    unconstr_demand_flight = 0.
    for p in range(len(itinerary_no)):
        unconstr_demand_flight = unconstr_demand_flight + (delta_i_p(i,p)*D_p_e(p))
    return unconstr_demand_flight

#Make function to get unconstrained business demand for flight i
def Q_i_b(i):
    unconstr_demand_flight = 0.
    for p in range(len(itinerary_no)):
        unconstr_demand_flight = unconstr_demand_flight + (delta_i_p(i,p)*D_p_b(p))
    return unconstr_demand_flight

def terminating_arc(n,k):
    a = 0
    for i in range(len(arcs[k])):
        if n == arcs[k][i][2]:
            a = arcs[k][i][0]
    return a
    






