# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 17:16:51 2019

@author: woute
"""
from tableaux2 import *
from Functions import *
from initial_solution2 import *
import gurobipy as grb


constr_p = []
constr_r = []

columns = {}
for p in range(len(itinerary_no)):
    columns[p] = [737]


# CREATE MODEL
m = grb.Model('MinPaxCost')


# DECISION VARIABLES
reallo     = {}    #t_p^r,k

for p in range(len(itinerary_no)):
    for r in list(columns[p]):
        k = 0
        reallo[p,r,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
              name="t_%s^{%s,%s}"%(p,r,k))
        reallo[r,p,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
              name="t_%s^{%s,%s}"%(p,r,k))  
    
m.update()
        
loop = True

while loop == True:
    k = 0
    obj = grb.quicksum(grb.quicksum((path_fare(p, k) - recap_rate(p, r, k) * path_fare(r, k)) * reallo[p,r,k] for r in list(columns[p])) for p in range(len(itinerary_no)))

    m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective
    
    m.update()    
    


    col_loop = True
    
    
    ### ADD COLUMNS ###
    while col_loop == True :
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
      
        ### CREATE DECISION VARIABLES ###########################################################################################
        for p in range(len(itinerary_no)):
            for r in list(columns[p]):
                k = 0
                reallo[p,r,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                      name="t_%s^{%s,%s}"%(p,r,k))
                reallo[r,p,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                      name="t_%s^{%s,%s}"%(r,p,k))                
        
        m.update()
        #        else:
        #            r = 737
        #            k = 0
        #            reallo[p,r,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
        #                      name="t_%s^{%s,%s}"%(p,r,k))
        
        
        
        
        ##### OBJECTIVE FUNCTION #################################################################################################
        
        obj = grb.quicksum(grb.quicksum((path_fare(p, k) - recap_rate(p, r, k) * path_fare(r, k)) * reallo[p,r,k] for r in list(columns[p])) for p in range(len(itinerary_no)))
        
        
        m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective
        
        m.update()
        m.write("model.lp")
        
        
        print "Objective function created."
        
        
        ##### CONSTRAINTS ########################################################################################################
        
        ### 1 ################################################################
        print "Constraint 1 loading"
        
        for f in range(len(flight_no)):
            k = 0
            m.addConstr(grb.quicksum(grb.quicksum(delta(f,p)*reallo[p,r,k] for r in list(columns[p])) for p in range(len(itinerary_no))) - grb.quicksum(grb.quicksum(delta(f,p)*recap_rate(r,p,k)*reallo[r,p,k] for r in list(columns[p]))for p in range(len(itinerary_no)))
                                ,GRB.GREATER_EQUAL,
                                    Q_CAP(f,k))                
        m.update()
        
        if len(constr_p) > 0.:
            for p in list(constr_p):
                r = constr_r[constr_p.index(p)]
    
                
                m.addConstr(reallo[p,r,0],
                                        GRB.LESS_EQUAL,
                                        D(p, 0))
        
        m.update()
        
        
        m.write("model1.lp")
         
        m.optimize()
        
        
        pi = [c.Pi for c in m.getConstrs()]
        
        sigma = pi[len(flight_no):(len(flight_no)+len(itinerary_no))]
        pi = pi[:len(flight_no)]
        c_pi.append([pi])    
#        for v in m.getVars():
#            if v.x > 0:
#                print (v.varName, v.x)    
        print ('Obj:', m.objVal)    
    
    
    
    
    while row_loop == True:
        col_loop = False
        row_loop = 0.
        p_row = []
        r_row = []
        for p in range(len(itinerary_no)):
            for r in list(columns[p]):
                if p == 592 and r == 737:
                    print "OF TOCH WEL?"
                
                if reallo[p,r,0].x > D(p, 0):
#                    it = 0.
                    
#                    for i in range(len(recapture_from)):
#                        for k in range(len(p_row)):
#                            if p_row[k] == recapture_from[i] and r_row[k] == recapture_to[i]:
#                                it = it + 1.
                    
#                    if it == 0.:
                    print p,r
                    p_row.append(p)
                    r_row.append(r)
                    row_loop = row_loop + 1
                    
                    m.addConstr(reallo[p,r,0],
                                    GRB.LESS_EQUAL,
                                    D(p, 0))
        
        m.update()
        
    
        m.write("model.lp")
     
        m.optimize()
        
        
        pi = [c.Pi for c in m.getConstrs()]
        
        sigma = pi[len(flight_no):(len(flight_no)+len(itinerary_no))]
        pi = pi[:len(flight_no)]
            
#        for v in m.getVars():
#            if v.x > 0:
#                print (v.varName, v.x)    
        print ('Obj:', m.objVal)


            
        print row_loop
        if row_loop == 0.:
            col_loop = True
            row_loop = False 
        
        for p in list(p_row):
            r = r_row[p_row.index(p)]
            constr_p.append(p)
            constr_r.append(r)  
#            
#            
#            m.addConstr(reallo[p,r,0],
#                                    GRB.LESS_EQUAL,
#                                    D(p, 0))
            

            
            
        


    
       
    print "hallo met gert"





    