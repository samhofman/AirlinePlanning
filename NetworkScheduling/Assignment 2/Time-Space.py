# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 11:42:35 2019

@author: woute
"""

from Input import *
from operator import itemgetter

#For each aircraft type k and for each airport, create list with in- and outgoing flights
#i.e. list with departure and arrival times





nodes = {}

for k in range(len(TAT)):
    nodes[k] = [0] * (len(airports))
    for a in range(len(airports)):
        nodes[k][a] = []
        for i in range(len(origin)):
            if airports[a] == origin[i]:
                nodes[k][a].append([int(arc_no[i]), 'd', flight_time[i][0]])    
            if airports[a] == destination[i]:
                if flight_time[i][1]+int(TAT[k]) > 1440:
                    nodes[k][a].append([int(arc_no[i]), 'a', flight_time[i][1]+int(TAT[k])-1440])
                else:
                    nodes[k][a].append([int(arc_no[i]), 'a', flight_time[i][1]+int(TAT[k])])
        nodes[k][a] = sorted(nodes[k][a], key=itemgetter(2))

time_space = {}
arcs = {}
night_arcs = {}


for k in range(len(TAT)):
    length = 0.
    night_arcs[k] = [0] * len(airports)
    for a in range(len(airports)):
        length = int(length + len(nodes[k][a]))
    time_space[k] = [0] * length
    arcs[k] = [0] * (length-1)        
    i = 0
    n = 0
    for a in range(len(airports)):
        for j in range(len(nodes[k][a])):
            time_space[k][i] = i, airports[a], nodes[k][a][j][2], nodes[k][a][j][1], nodes[k][a][j][0]
            if j == 0:
                start = i
            if i <= (length-2):
                arcs[k][i] = i, i, i + 1
            if j == (len(nodes[k][a])-1):
                night_arcs[k][n] = i, i, start
                n = n + 1
            i = i + 1
        
for k in range(len(TAT)):
    for i in range(len(arcs[k])):
        for j in range(len(night_arcs[k])):
            if arcs[k][i][0] == night_arcs[k][j][0]:
                arcs[k][i] = night_arcs[k][j]
    arcs[k].append(night_arcs[k][-1])

                    