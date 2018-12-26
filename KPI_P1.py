# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 21:11:08 2018

@author: woute
"""

from OF_P1 import *

KPI = np.array(['FROM', 'TO', 'Distance', 'Seats', 'Pax', 'ASK', 'RPK'])
KPI_values = []

       
for i in range(nodes):
    for j in range(nodes):
            total_seats = grb.LinExpr.getValue(grb.quicksum(flights[i,j,k].x * seats[0][k] for k in range(commod)))
            ASKij = distance(i,j) * total_seats
            RPKij = grb.LinExpr.getValue(distance(i,j) * flow[i,j])
            if RPKij > 0.:
                KPI_values = np.array([i,j,distance(i,j),total_seats, flow[i,j].x,ASKij,RPKij])
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

            