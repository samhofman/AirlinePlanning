# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 17:50:22 2019

@author: hofma
"""

from Crew_Pairing_Input import *
from math import *

#Make functions that return flight origin of flight i
def flight_origin_737(i):
    origin = 'ERROR'
    for j in range(len(flight_no_737)):
        if arc_no_737[j][0] == i:
            origin = flight_no_737[j][1]
            break
    return origin

#Make functions that return flight destination of flight i
def flight_destin_737(i):
    destin = 'ERROR'
    for j in range(len(flight_no_737)):
        if arc_no_737[j][0] == i:
            destin = flight_no_737[j][2]
            break
    return destin

#Make functions that return time between an arriving and departing flight
def idle_time_737(i,j): #i arriving flight, j departing flight
    idle = 0.
    a = 0
    b = 0
    if i < arc_no_737[0][0] or j < arc_no_737[0][0]:
        return 'ERROR'
        quit
    for m in range(len(flight_no_737)):
        if arc_no_737[m][0] == i:
            a = m
        elif arc_no_737[m][0] == j:
            b = m
    idle = flight_time_737[b][0] - flight_time_737[a][1]
    if idle < 0.: #If arriving flight is before midnight and departing after midnight
        idle = flight_time_737[b][0] + 1440. - flight_time_737[a][1]
    return idle

def flight_number_737(i):
    fnum = 'ERROR'
    for j in range(len(flight_no_737)):
        if arc_no_737[j][0] == i:
            fnum = flight_no_737[j][0]
            break
    return fnum

#Make functions that return flight time
def f_time_737(i):
    time = 0.
    a = 0
    if i < arc_no_737[0][0]:
        return 'ERROR'
        quit
    for m in range(len(flight_no_737)):
        if arc_no_737[m][0] == i:
            a = m
    time = flight_time_737[a][1] - flight_time_737[a][0]
    if time < 0.: #If arriving flight is before midnight and departing after midnight
        time = flight_time_737[a][1] + 1440. - flight_time_737[a][0]
    return time

#Make function that returns whether pairing is still feasible

##### For the B737 #####

def Pairing_function_737(testpairing,i):
    TAFB_10hours = True
    base_start_end = True
    duty_4flights = True
    idletime_30_180 = True
    TAFB = 0.       #Hours away from base
    idletime = 0.       #Time between flights
    pairing_list = list(testpairing[i])       #Convert to list to be able to find index of j
    #Calculate flights per duty (cannot be higher than 4)
    if len(testpairing[i]) > 4:
        duty_4flights = False
    #Calculate TAFB (cannot be higher than 10 hours)
    for j in testpairing[i]:
        index = pairing_list.index(j)
        if index == 0:      #First flight in pairing
            TAFB = f_time_737(j)        #TAFB = flight time of first flight
            if TAFB > 600.:         #TAFB cannot be higher than 10 hours (600 minutes)
                    TAFB_10hours = False
                    break
        elif index > 0:         #Next flights            
            if flight_destin_737(j) != 'AEP':       #Flight not going to base
                #TAFB = previous TAFB + flight time + idle time between this and previous flight
                TAFB = TAFB + f_time_737(j) + idle_time_737(testpairing[i][index-1],j)
                if TAFB > 600.:         #TAFB cannot be higher than 10 hours (600 minutes)
                    TAFB_10hours = False
                    break
            elif flight_destin_737(j) == 'AEP':         #Flight going to base
                #First calculate TAFB
                TAFB = TAFB + f_time_737(j) + idle_time_737(testpairing[i][index-1],j)
                if TAFB > 600.:         #TAFB cannot be higher than 10 hours (600 minutes)
                    TAFB_10hours = False
                    break
                #Then reset TAFB
                TAFB = 0.
    #Calculate time between flights (must be between 30 and 180 minutes)
    for k in testpairing[i]:
        index = pairing_list.index(k)
        if index == 0:      #First flight in pairing
            continue        #No idle time possible yet
        elif index > 0:         #Next flights
            idletime = idle_time_737(testpairing[i][index-1],k)
            if idletime < 30. or idletime > 180.:
                idletime_30_180 = False
                break
    return TAFB_10hours, duty_4flights, idletime_30_180 

#TEST
#testpairing = [[209,210,209,210]]
#pairing_list = list(testpairing[0])
#for k in testpairing[0]:
#        index = pairing_list.index(k)
#        print index
#        if index == 0:      #First flight in pairing
#            print 'Continue'
#            continue        #No idle time possible yet
#        elif index > 0:         #Next flights
#            idletime = idle_time_737(testpairing[0][index-1],k)
#            print idletime
#            if idletime < 30. or idletime > 180.:
#                idletime_30_180 = False
#                print 'False'
#                break

