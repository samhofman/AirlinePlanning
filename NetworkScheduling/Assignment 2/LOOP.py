# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 18:10:20 2019

@author: woute
"""

from Initial_Solution import *

i = 0

add_col_a = {}
add_col_b = {}
add_col_c = {}
r_obj = {}

for p in range(len(itinerary_no)):
    add_col_a[p] = [771]
    add_col_b[p] = [771]
    add_col_c[p] = [771]

    
for a in list([0, 1, 2]):
    for p in range(len(recapture_from_to)):
        for r in range(len(recapture_from_to)):
            if p == recapture_from_to[r][0]:
                if add_col(a,p, recapture_from_to[r][1]) < 0:
                    #Same procedure for each constraint 4a,b or c
                    if a == 0:
                        it = 0.
                        
                        #Check whether a flight is added double
                        for k in range(len(add_col_a[p])):
                            if recapture_from_to[r][1] == add_col_a[p][k]:
                                it = it + 1
                        #If not: add column
                        if it == 0.:
                            add_col_a[p].append(recapture_from_to[r][1])

                    if a == 1:
                        it = 0.
                        
                        for k in range(len(add_col_b[p])):
                            if recapture_from_to[r][1] == add_col_b[p][k]:
                                it = it + 1
                        
                        if it == 0.:
                            add_col_b[p].append(r)
                            
                    if a == 2:
                        it = 0.
                        
                        for k in range(len(add_col_c[p])):
                            if recapture_from_to[r][1] == add_col_c[p][k]:
                                it = it + 1
                        
                        if it == 0.:
                            add_col_c[p].append(r) 

#separate list r_obj for all r's to put in objective function (add_col_a and add_col_c)
for p in range(len(itinerary_no)):
    r_obj[p] = add_col_a[p]+add_col_c[p]
    r_obj[p] = list(set(r_obj[p]))

    
for p in range(len(itinerary_no)):
    ec_sum = 0.
    bs_sum = 0.
    bus_sum = 0.
    for r in list(add_col_a[p]):
        ec_sum = ec_sum + tpre[p,r].x
        if ec_sum > D_p_e(p):
            print 'row_ec'
    for r in list(add_col_b[p]):
        bs_sum = bs_sum + tprb[p,r].x
        if bs_sum > D_p_b(p):
            print 'row_bs'
    for r in list(add_col_c[p]):
        bus_sum = bus_sum + tpre[p,r].x
        if bus_sum > D_p_e(p):
            print 'bus_row'




