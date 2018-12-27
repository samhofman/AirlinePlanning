# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 21:11:08 2018

@author: woute
"""

from OF_P1 import *

KPI = np.array(['FROM', 'TO', 'Distance', 'Seats', 'Pax', 'ASK', 'RPK', ' ', 'RASK', 'CASK', 'Yield'])
KPI_values = []

       
for i in range(nodes):
    for j in range(nodes):
        total_seats = grb.LinExpr.getValue(grb.quicksum(flights[i,j,k].x * seats[0][k] for k in range(commod)))
        ASKij = distance(i,j) * total_seats
        RPKij = grb.LinExpr.getValue(distance(i,j) * (flow[i,j]+hflow[i,j]))
        revenueij  = grb.LinExpr.getValue((5.9*dist_fact(i,j)+0.043)*distance(i,j)*(hflow[i,j] + flow[i,j]))
        costij = grb.LinExpr.getValue(grb.quicksum((flights[i,j,k]*cost_fact(i,j)*(Cx_ar[0][k]+Ct[0][k]*distance(i,j)/speed[0][k]+Cf[0][k]*F17*distance(i,j)/1.5)) for k in range(commod)) + grb.quicksum(AC[0][k]*Cl[0][k] for k in range(commod)))
        if ASKij > 0. and RPKij > 0.:    
            RASK = revenueij/ASKij
            CASK  = costij/ASKij
            yieldij =  revenueij/RPKij
            KPI_values = np.array([i,j,distance(i,j),total_seats, flow[i,j].x,ASKij,RPKij, ' ', RASK, CASK, yieldij])
            KPI = np.vstack( (KPI, KPI_values))

with open('KPI_P1_results.csv', 'wb') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerows(KPI)




#var_ASK = []    
#var_RPK = []
#
#
#for var in m.getVars():
#    # Or use list comprehensions instead 
#    
#    if 'APK' == str(var.VarName[0]) and var.x > 0:
#        var_ASK.append([var.VarName, var.x]) 
#    if 'RPK' == str(var.VarName[0]) and var.x > 0:
#        var_RPK.append([var.VarName, var.x])    
## Write to csv
#with open('KPI_P1.csv', 'wb') as myfile:
#     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
#     wr.writerows(var_ASK)
#     wr.writerows(var_RPK)

            