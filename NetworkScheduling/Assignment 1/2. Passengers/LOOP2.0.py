# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 14:10:38 2019

@author: woute
"""

from tableaux2 import *
from Functions import *
from initial_solution2 import *
import gurobipy as grb
import csv
import sys
import time

start = time.time()


constr_p = []
constr_r = []

columns = {}
for p in range(len(itinerary_no)):
    columns[p] = [737]
    

loop = True
col_loop = True
col_count = 0

while loop == True:
    
    
    while col_loop == True:
        print "Column loop"
        row_loop = False
        col_loop = 0.
        
        for p in range(len(itinerary_no)):
            for c in range(len(recapture_from_to)):
                if p == recapture_from_to[c][0]:
                    if add_col_init(p, recapture_from_to[c][1]) < 0.:
                        it = 0.
                        
                        for k in range(len(columns[p])):
                            if recapture_from_to[c][1] == columns[p][k]:
                                it = it + 1
                        if it == 0.:
                            columns[p].append(recapture_from_to[c][1])    
                            col_loop = col_loop + 1
                            
        if col_loop == 0.:
            row_loop = True
            col_loop = False
            col_count = 1
            
        optimize = True
    
    while optimize == True:
        
        m = grb.Model('MinCost')
        
        ### CREATE DECISION VARIABLES ###
        reallo = {}
        
        for p in range(len(itinerary_no)):
            for r in list(columns[p]):
                k = 0
                reallo[p,r,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                      name="t_%s^{%s,%s}"%(p,r,k))
                reallo[r,p,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                      name="t_%s^{%s,%s}"%(r,p,k))                  
        m.update()
            
        ##### OBJECTIVE FUNCTION ###
        obj = grb.quicksum(grb.quicksum((path_fare(p, k) - recap_rate(p, r, k) * path_fare(r, k)) * reallo[p,r,k] for r in list(columns[p])) for p in range(len(itinerary_no)))
        
        
        m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective
        
        m.update()
        m.write("model.lp")
        
        
        print "Objective function created."
            
        ##### CONSTRAINTS ###        
        ### 1 ###
        print "Constraint 1 loading"
        
        for f in range(len(flight_no)):
            k = 0
            m.addConstr(grb.quicksum(grb.quicksum(delta(f,p)*reallo[p,r,k] for r in list(columns[p])) for p in range(len(itinerary_no))) - grb.quicksum(grb.quicksum(delta(f,p)*recap_rate(r,p,k)*reallo[r,p,k] for r in list(columns[p]))for p in range(len(itinerary_no)))
                                ,GRB.GREATER_EQUAL,
                                    Q_CAP(f,k))                
        m.update()
        
        ### 2 ###        
        if len(constr_p) > 0.:
            for k in range(len(constr_p)):
                p = constr_p[k]
                r = constr_r[k]
    
                
                m.addConstr(grb.quicksum(reallo[p,r,0] for r in list(columns[p])),
                                        GRB.LESS_EQUAL,
                                        D(p, 0))
        
        m.update()
        
        m.write("model.lp")
         
        m.optimize()            
            
        pi = [c.Pi for c in m.getConstrs()]
        
        sigma = pi[len(flight_no):(len(flight_no)+len(itinerary_no))]
        pi = pi[:len(flight_no)]
    
        for v in m.getVars():
            if v.x > 0:
                print (v.varName, v.x)    
        print ('Obj:', m.objVal)    
        
        
        if m.objVal == 335204.9:
            var = []
            for v in m.getVars():
                if v.x > 0:
                    var.append([v.varName, v.x])
            with open('Results.csv', 'wb') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerows(var)
            with open('Duals.csv', 'wb') as myfile:
                wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
                wr.writerows([pi, sigma])
            end = time.time() 
            print end - start                   
            sys.exit()
            
        optimize = False
        
        if col_count == 1:
            row_loop = True
            col_count = 0
        
        else:
            col_loop = True
        

    while row_loop == True:
        print "Row Loop"
        
        col_loop = False
        row_loop = 0.
        p_row = []
        r_row = []
        for p in range(len(itinerary_no)):
            reallosum = 0.
            for r in list(columns[p]):
                reallosum = reallosum + reallo[p,r,0].x
                if reallosum > D(p, 0):
                    print p, r, D(p,0)
                    constr_p.append(p)
                    constr_r.append(r)
                    
                    row_loop = row_loop + 1
        
        if row_loop == 0.:
            col_loop = True
            row_loop = False                    
                    
        optimize = True
        row_loop = False
        
                    
                    
                    
                    
                    
                    
                    
                    

        
        