# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 21:11:08 2018

@author: woute
"""

from OF_P1 import *


### GET TOTAL PASSENGERS ON ROUTE -> x + w 

transfer_pax  = np.zeros(shape=(nodes,nodes))
pax_per_route = np.zeros(shape=(nodes,nodes))

for i in range(nodes):
    for j in range(nodes):
        transfer_pax[i][j] = hflow[i,j].x
        if transfer_pax[i][j] > 0.:
            transfer_pax[i][0] = transfer_pax[i][0] + transfer_pax[i][j]
            transfer_pax[0][j] = transfer_pax[0][j] + transfer_pax[i][j]
            transfer_pax[i][j] = 0

for i in range(nodes):
    for j in range(nodes):
        pax_per_route[i][j] = flow[i,j].x + transfer_pax[i][j]

### CALCULATE KPIs

KPI = np.array(['From','To', 'Distance', 'Seats', 'Passengers','ASK','RPK', 'cost','revenue', 'RASK', 'CASK', 'Yield'])
KPI_values = []
tot_dist = 0.
tot_seats = 0.
tot_pax = 0.
tot_ASK = 0.
tot_RPK = 0.
tot_cost = 0.
tot_rev = 0.

for i in range (nodes):
    for j in range(nodes):
        if pax_per_route[i][j] > 0.:
            seats_available = grb.LinExpr.getValue(grb.quicksum(flights[i,j,k].x * seats[0][k] for k in range(commod)))
            
            ASK = distance(i,j) * seats_available
            RPK = distance(i,j) * pax_per_route[i][j]
        
        
            revenue = grb.LinExpr.getValue((5.9*dist_fact(i,j)+0.043)*distance(i,j)*(hflow[i,j] + flow[i,j]))
            costs   = grb.LinExpr.getValue(grb.quicksum((flights[i,j,k].x*cost_fact(i,j)*(Cx_ar[0][k]+Ct[0][k]*distance(i,j)/speed[0][k]+Cf[0][k]*F17*distance(i,j)/1.5)) for k in range(commod)))
    
            RASK  = revenue/ASK
            CASK  = costs/ASK
            YIELD = revenue/RPK
                        
            tot_dist = tot_dist + distance(i,j)
            tot_seats = tot_seats + seats_available
            tot_pax = tot_pax + pax_per_route[i][j]
            tot_cost = tot_cost + costs
            tot_rev = tot_rev + revenue
            tot_ASK = tot_ASK + ASK
            tot_RPK = tot_RPK + RPK
        
                
            KPI_values = np.array([i,j,distance(i,j),seats_available, pax_per_route[i][j], ASK, RPK, costs, revenue, RASK, CASK, YIELD])
            KPI = np.vstack( (KPI, KPI_values))

KPI_tot = np.array(['TOTAL', '', tot_dist, tot_seats, tot_pax, tot_ASK, tot_RPK, tot_cost, tot_rev, tot_rev/tot_ASK, tot_cost/tot_ASK, tot_rev/tot_RPK])        
KPI = np.vstack( (KPI, KPI_tot))

### CASK in miles and dollar

COST_USD = tot_cost * 1.25   #convert to USD (2003-2005)
ASM = tot_ASK * 0.621371192 #convert to miles


with open('KPI_P1_results.csv', 'wb') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerows(KPI)






            