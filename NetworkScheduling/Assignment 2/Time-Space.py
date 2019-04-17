# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 11:42:35 2019

@author: woute
"""


from Input import *
from operator import itemgetter


#Create list with times of in- and outgoing flights (nodes)
#List: nodes = [flight_nr, a arriving/d departing, flight time]

nodes = {}

for k in range(len(TAT)):                                                                           #Separate list for each fleet type k
    nodes[k] = [0] * (len(airports))                                                                #Generate empty list for each airport within nodes[k]
    for a in range(len(airports)):                                                                  #For each airport:
        nodes[k][a] = []                                                                            ###Initiate empty list
        for i in range(len(origin)):                                                                ###Run through all flights
            if airports[a] == origin[i]:                                                            #####Check for each airport if it's the origin of a flight
                nodes[k][a].append([int(arc_no[i]), 'd', flight_time[i][0]])                        #######If so: add flight nr, d for departure and departure time    
            if airports[a] == destination[i]:                                                       #####Check for each airport if it's the destination of a flight
                if flight_time[i][1]+int(TAT[k]) > 1440:                                            #######If so: add flight nr, a for arrival and arrival time+TAT
                    nodes[k][a].append([int(arc_no[i]), 'a', flight_time[i][1]+int(TAT[k])-1440])   #######If arrival time+TAT > 1440 minutes (midnight):
                else:                                                                               #########Set time to beginning of the day (arrival time+TAT - 1440)
                    nodes[k][a].append([int(arc_no[i]), 'a', flight_time[i][1]+int(TAT[k])])
        nodes[k][a] = sorted(nodes[k][a], key=itemgetter(2))                                        ###Sort times chronologically

#Create time-space network and ground arcs

#time_space = [arc nr, airport, time, arriving/departing, flight nr.]
time_space = {}                                                                                     #Create empty list for the time-space network
#arcs = [arc nr, originating node, terminating node]
arcs = {}                                                                                           #Create empty list for the ground arcs (incl. overnight arcs)
#night_arcs = [arc nr, orignating node (last time point of the day), terminating node (first time point of the day)]
night_arcs = {}                                                                                     #Create empty list for the overnight arcs


for k in range(len(TAT)):                                                                           #For each fleet type k
    length = 0                                                                                      ###Initiate counting total amount of times (arrival and departure) at airports
    night_arcs[k] = [0] * len(airports)                                                             ###Initiate lists in overnight arcs list (arc, ending node, starting node)
    for a in range(len(airports)):                                                                  ###Count total amount of times
        length = int(length + len(nodes[k][a]))
    time_space[k] = [0] * length                                                                    ###Initiate time-space network list
    arcs[k] = [0] * (length-1)                                                                      ###Initiate ground arcs list
    i = 0
    n = 0
    for a in range(len(airports)):                                                                  ###For each airport in the nodes list
        for j in range(len(nodes[k][a])):                                                           #####For each time for the airports in nodes list
            time_space[k][i] = i, airports[a], nodes[k][a][j][2], nodes[k][a][j][1], nodes[k][a][j][0]#####time-space network list = [arc nr, airport, time, arriving/departing, flight nr.]
            if j == 0:                                                                              #######remember starting node for each airport to obtain overnight arcs
                start = i
            if i <= (length-2):                                                                     #######link arc nr. with nodes it connects
                arcs[k][i] = i, i, i + 1
            if j == (len(nodes[k][a])-1):                                                           #######at each last time point, create overnight arc item
                night_arcs[k][n] = i, i, start
                n = n + 1
            i = i + 1

#Overnight arcs need to be replaced in the arc list since these are not yet accounted for  

for k in range(len(TAT)):                                                                           #For each fleet type k
    for i in range(len(arcs[k])):                                                                   ###For each arc in fleet type k
        for j in range(len(night_arcs[k])):                                                         #####For each overnight arc
            if arcs[k][i][0] == night_arcs[k][j][0]:                                                #######Replace overnight arcs with correct starting node
                arcs[k][i] = night_arcs[k][j]
    arcs[k].append(night_arcs[k][-1])                                                               ###Final overnight arc needs to be since it has not been generated in the arcs loop    

                    