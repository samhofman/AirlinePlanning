# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 12:53:57 2019

@author: woute
"""
##### RESULTS #####
#OBJ = 3399056,33202
# 58 columns
# 507 rows
### -> 164 economy
### -> 343 business

from Initial_Solution import *
import gurobipy as grb
import csv
from math import *
from Functions import *
from Input import *
from Time_Space import *
import sys
import time

GRB = grb.GRB


###Lists and parameters to use in iterations and solution ###

#lists to define which sigma for which constraint
p_sigmae = []
p_sigmab = []

#List for which constraints 5a and 5b have to be made
constr_p_a = []
constr_p_b = []

constr_r_a = []
constr_r_b = []

#List with columns to be added
add_col_a = {}
add_col_b = {}
add_col_c = {}


r_obj     = {}

#Initiate lists with itinerary 771
for p in range(len(itinerary_no)):
    add_col_a[p] = [771]
    add_col_b[p] = [771]
    add_col_c[p] = [771]
    
loop = True
col_loop = True
col_count = 0
cols = 0
rows = 0
iters = 0
z = 0


col_loop_a = 0.
col_loop_b = 0.
col_loop_c = 0.
row_loop_a = 0.
row_loop_b = 0.


col_list = []
row_list = []


#Initiate Iteration loop
while loop == True:
    
    #Initiate column generation loop
    while col_loop == True:
        print "Column loop"
        row_loop = False
        col_loop_a = 0.
        col_loop_b = 0.
        col_loop_c = 0.
        stop = 0.
        
        #Check whether to add columns for each itinerary
        for a in list([0, 1, 2]):                       #0,1,2 stand for 4a, 4b and 4c
            for p in range(len(recapture_from_to)):
                for r in range(len(recapture_from_to)):
                    if p == recapture_from_to[r][0]:
                        
                        #Definition add_col from Initial_solution -> check price out
                        if add_col(a,p, recapture_from_to[r][1],p_sigmae,p_sigmab,sigma_e,sigma_b,pi_fe,pi_fb,pi_b) < 0:
                            
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
                                    col_loop_a = col_loop_a + 1
                                    cols = cols + 1 #count total amount of columns added
                                    
                            if a == 1:
                                it = 0.
                                
                                for k in range(len(add_col_b[p])):
                                    if recapture_from_to[r][1] == add_col_b[p][k]:
                                        it = it + 1
                                
                                if it == 0.:
                                    add_col_b[p].append(recapture_from_to[r][1])
                                    col_loop_b = col_loop_b + 1
                                    cols = cols + 1 #count total amount of columns added
                                    
                            if a == 2:
                                it = 0.
                                
                                for k in range(len(add_col_c[p])):
                                    if recapture_from_to[r][1] == add_col_c[p][k]:
                                        it = it + 1
                                
                                if it == 0.:
                                    add_col_c[p].append(recapture_from_to[r][1]) 
                                    col_loop_c = col_loop_c + 1
                                    cols = cols + 1 #count total amount of columns added
        
        #separate list r_obj for all r's to put in objective function (add_col_a and add_col_c)
        for p in range(len(itinerary_no)):
            r_obj[p] = add_col_a[p]+add_col_c[p]
            r_obj[p] = list(set(r_obj[p]))        
        
        
        print 'columns:', (col_loop_a + col_loop_b + col_loop_c)
#        col_list.append(col_loop_a + col_loop_b + col_loop_c)
        
        #If no columns added anymore, continue to check whether to add rows
        if (col_loop_a + col_loop_b + col_loop_c) == 0.:
            row_loop = True
            col_loop = False
            col_count = 1.
            stop = stop + 1.  #check to quit the loop, if no rows AND no columns added -> finished  
        

        col_loop = False
        optimize = True
        
    #When column added or row added -> Optimize
    while optimize == True:
        
        print 'Optimize loop'
        
        # CREATE MODEL
        m = grb.Model('MinAllocCost')
        
        # DECISION VARIABLES
        tpre     = {}    #t_p^r,e
        tprb     = {}    #t_p^r,b
        fik     = {}    #f_i^k
        yak      = {}    #y_a^k 
        
        ### CREATE INITIAL DECISION VARIABLES ###########################################################################################
        
        #t_p^r for economy
        for p in range(len(itinerary_no)):
            for r in list(r_obj[p]):
                tpre[p,r] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                name="t_%s^{%s,e}"%(p,r))
                tpre[r,p] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                name="t_%s^{%s,e}"%(r,p))
            for r in list(constr_r_a):
                tpre[p,r] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                name="t_%s^{%s,e}"%(p,r))
                tpre[r,p] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                name="t_%s^{%s,e}"%(r,p))            
        
        #t_p^r for business    
        for p in range(len(itinerary_no)):                        
            tprb[p,771] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, #Only spill business pax to fictitious itinerary
            name="t_%s^{771,b}"%(p))
            
            
        #f_i^k
        for i in Lfbis:      #Take fictitious itinerary into account
            for k in range(len(k_units)):
                fik[i,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
            name="f_%s^{%s}"%(i,k))
                
        #y_a^k
        for k in range(len(k_units)):
            for a in range(len(arcs[k])):
                yak[a,k] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
            name="y_%s^{%s}"%(a,k))
                
        m.update()        
        ##### OBJECTIVE FUNCTION #################################################################################################
        
        obj = grb.quicksum(grb.quicksum(costki(k,i)*fik[i,k] for k in range(len(k_units))) for i in Lfbis) \
        + grb.quicksum(grb.quicksum(((fare_e(p)-(b_p_r(p,r)*fare_e(r)))*tpre[p,r]) for r in list(r_obj[p])) for p in range(len(itinerary_no))) \
        + grb.quicksum(fare_b(p)*tprb[p,771] for p in range(len(itinerary_no))) \
        + (24.*4500.)
        
        m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective
        
        m.update()
        m.write("model.lp")
        
        print "Objective function created."    
            
        ##### CONSTRAINTS ########################################################################################################
        
        ### 1a ################################################################
        print "Constraint 1a loading"
        
        for i in Lf:
            m.addConstr(grb.quicksum(fik[i,k] for k in range(len(k_units)))
                                    ,GRB.EQUAL,
                                        1.)
        
        ### 1b ################################################################
        print "Constraint 1b loading"
        
        for k in range(len(k_units)):
            i = 232
            m.addConstr(fik[i,k]
                                    ,GRB.EQUAL,
                                        0.)
        
        ### 2 ################################################################
        print "Constraint 2 loading"
        
        for k in range(len(k_units)):
            for n in range(len(Ikn_set[k])):
                m.addConstr(yak[n,k] + fik[Okn_set[k][n],k] - yak[terminating_arc(n,k),k] - fik[Ikn_set[k][n],k],
                            GRB.EQUAL,
                            0.)
        
        ### 3 ################################################################
        print "Constraint 3 loading"
        
        for k in range(len(k_units)):
            NG = [] #Make list of ground arcs per k
            for n in range(len(night_arcs[k])):
                a = night_arcs[k][n][0]
                NG.append(a)
            m.addConstr(grb.quicksum(yak[a,k] for a in NG), #Make constraint per k
                                    GRB.LESS_EQUAL,
                                        AC_k(k))
        
        NG = [] #Clear list
        
        ### 4a ################################################################
        print "Constraint 4a loading"
        
        for i in Lf:
            m.addConstr(grb.quicksum((s_k_e(k)*fik[i,k]) for k in range(len(k_units))) \
                        + grb.quicksum(grb.quicksum((delta_i_p(i,p)*tpre[p,r]) for p in range(len(itinerary_no))) for r in list(add_col_a[p])) \
                        - grb.quicksum(grb.quicksum((delta_i_p(i,p)*b_p_r(r,p)*tpre[r,p]) for p in range(len(itinerary_no))) for r in list(add_col_a[p])),
                                    GRB.GREATER_EQUAL,
                                        Q_i_e(i))
            
        ### 4b ################################################################
        print "Constraint 4b loading"
        
        for i in Lf:
            m.addConstr(grb.quicksum((s_k_b(k)*fik[i,k]) for k in range(len(k_units))) \
                        + grb.quicksum((delta_i_p(i,p)*tprb[p,771]) for p in range(len(itinerary_no))),
                                    GRB.GREATER_EQUAL,
                                        Q_i_b(i))    
        
        ### 4c ################################################################
        print "Constraint 4c loading"
        
        for i in Lb:
            m.addConstr(216 + grb.quicksum(grb.quicksum((delta_i_p(i,p)*tpre[p,r]) for p in range(len(itinerary_no))) for r in list(add_col_c[p])) \
                        - grb.quicksum(grb.quicksum((delta_i_p(i,p)*b_p_r(r,p)*tpre[r,p]) for p in range(len(itinerary_no))) for r in list(add_col_c[p])) + grb.quicksum((delta_i_p(i,p)*tprb[p,771]) for p in range(len(itinerary_no))),
                                    GRB.GREATER_EQUAL,
                                        (Q_i_e(i) + Q_i_b(i)))
            
        ### 5a ################################################################
        print "Constraint 5a loading"
        
        if len(constr_p_a) > 0.:
            for k in range(len(constr_p_a)):
                p = constr_p_a[k]
                r = constr_r_a[k]
                m.addConstr(grb.quicksum(tpre[p,r] for r in list(r_obj[p])),
                            GRB.LESS_EQUAL,
                            D_p_e(p))
            
        ### 5b ################################################################
        print "Constraint 5b loading"
        
        if len(constr_p_b) > 0.:
            for k in range(len(constr_p_b)):
                p = constr_p_b[k]
                r = constr_r_b[k]
                
                m.addConstr(tprb[p,771],
                        GRB.LESS_EQUAL,
                        D_p_b(p))
        
        ### Run 
        m.update()   
        m.write("model.lp")
        
        m.optimize()
#        cont = 0
#        bina = 0
#        for v in m.getVars():
#            if 'f' == str(v.VarName[0]) and v.x > 0:
#                if v.x < 1.:
#                    cont = cont + 1
#                elif v.x == 1.:
#                    bina = bina + 1
                #print (v.varName, v.x)    
#        print 'total:', (cont + bina) 
#        print 'cont: ', cont
#        print 'bin:  ', bina
        print ('Obj:', m.objVal)        

        
        #count iterations
        iters = iters + 1
        
        #Get dual variables
        pi = [c.Pi for c in m.getConstrs()]
        
        pi_fe = pi[1880:1880+len(Lf)]
        pi_fb = pi[1880+len(Lf):1880+len(Lf)+len(Lf)]
        pi_b = pi[1880+len(Lf)+len(Lf):1880+len(Lf)+len(Lf)+len(Lb)]
        sigma_e = pi[1880+len(Lf)+len(Lf)+len(Lb):1880+len(Lf)+len(Lf)+len(Lb)+len(p_sigmae)]
        sigma_b = pi[1880+len(Lf)+len(Lf)+len(Lb)+len(p_sigmae):1880+len(Lf)+len(Lf)+len(Lb)+len(p_sigmae)+len(p_sigmab)]
        
        
        print 'optimized'
        
        
        #Create lists of objective values, added columns and added rows per iteration
        obj_list.append(m.objVal)
        col_list.append(col_loop_a + col_loop_b + col_loop_c)
        row_list.append(row_loop_a + row_loop_b)
        
        
        optimize = False
        
        #If column loop previously ran, run row loop
        if col_count == 1.:
            row_loop = True
            col_count = 0.
        
        else:
#            obj_list.append(m.objVal)
            col_loop = True
        
### Row generation loop ###
            
    while row_loop == True:
        print "Row Loop" 
        
        col_loop = False
        
        #Start counting whether rows are added
        
        row_loop_a = 0.
        row_loop_b = 0.
        p_sigma = []
        
        #For each itinerary check whether constraint 5a and 5b are violated
        for p in range(len(itinerary_no)):
            ec_sum = 0.
            bs_sum = 0.
            bus_sum = 0.
            for r in list(add_col_a[p]):
                ec_sum = ec_sum + tpre[p,r].x #sum amount of economy passengers in path
                if ec_sum > D_p_e(p):
                    #print p, r, D_p_e(p)
                    
                    #Store p and r for which constraint 5a has to be added
                    constr_p_a.append(p)
                    constr_r_a.append(r)
                    rows = rows + 1
                    row_loop_a = row_loop_a + 1
                    p_sigmae.append(p)
            for r in list(add_col_b[p]):
                #bs_sum = bs_sum + tprb[p,771].x
                if tprb[p,771].x > D_p_b(p):
                    #print p, r, D_p_b(p)
                    
                    #Store p and r for which constraint 5b has to be added
                    it = 0.
                    
                    for k in range(len(constr_p_b)):
                        if p == constr_p_b[k]:
                            it = it + 1
                    
                    if it == 0.:                    
                        constr_p_b.append(p)
                        constr_r_b.append(771)
                        rows = rows + 1
                        row_loop_b = row_loop_b + 1
                        p_sigmab.append(p)


        print 'rows:', (row_loop_a + row_loop_b)
#        row_list.append(row_loop_a + row_loop_b)
        

        #If no rows added -> optimize and go to column loop               
        if row_loop_a + row_loop_b == 0.:
            col_loop = True
            row_loop = False
            stop = stop + 1. 
            
            
      
        #If no rows and columns added -> optimal solution found, Jump out of loop
        if stop == 2.:
            t_end = time.time()
            loop = False
            row_loop = False
            column_loop = False
            optimize = False
            print 'final obj', m.objVal
            
            
        optimize = True
        row_loop = False
        #col_loop = False
            
        
        
print "Generating results"   

fres = []
yres = []
teres = []
tbres = []


for v in m.getVars():
    if 'f' == str(v.varName[0]) and v.x > 0:
        fres.append([v.varName, v.x])
    if 'y' == str(v.varName[0]) and v.x > 0:
        yres.append([v.varName, v.x])        
    if 't' == str(v.varName[0]) and 'e' == str(v.varName[-2]) and v.x > 0:
        teres.append([v.varName, v.x])
    if 't' == str(v.varName[0]) and 'b' == str(v.varName[-2]) and v.x > 0:
        tbres.append([v.varName, v.x])        
    
with open('RES_ground_arcs.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(yres) 

with open('RES_flights.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(fres)

with open('RES_ec_reallocation_iteration.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(teres)     

with open('RES_bus_reallocation.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(tbres)

with open('Dual.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows([pi_fe, pi_fb, pi_b, p_sigmae, sigma_e, p_sigmab, sigma_b])     

print 'runtime:', (t_end-t_start)
print 'iterations:', iters
print '#fik:', len(fres)
print '#yak:', len(yres)
print '#tpre:', len(teres)
print '#tprb:', len(tbres)
print 'columns:', cols
print 'rows:', rows

        