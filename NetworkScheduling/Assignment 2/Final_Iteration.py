# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 14:51:11 2019

@author: woute
"""

from Iteration import *
import gurobipy as grb

raw_input = ('Hit Enter to continue')

row_loop = True


#Same as 'Iteration.py'

while row_loop == True:

    m = grb.Model('MinAllocCost')
    
    # DECISION VARIABLES
    tpre     = {}    #t_p^r,e
    tprb     = {}    #t_p^r,b
    fik      = {}    #f_i^k
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
            fik[i,k] = m.addVar(vtype=GRB.INTEGER, lb=0,
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
    obj_list.append(m.objVal)
    iters = iters + 1.


    
    print "Row Loop" 
        
    row_loop_a = 0.
    row_loop_b = 0.
    
    for p in range(len(itinerary_no)):
        ec_sum = 0.
        bs_sum = 0.
        bus_sum = 0.
        for r in list(add_col_a[p]):
            ec_sum = ec_sum + tpre[p,r].x
            if ec_sum > D_p_e(p):
                #print p, r, D_p_e(p)
                it = 0.
                for k in range(len(constr_p_a)):
                    if p == constr_p_a[k]:
                        it = it + 1
                
                if it == 0.:
                    constr_p_a.append(p)
                    constr_r_a.append(r)
                    rows = rows + 1
                    row_loop_a = row_loop_a + 1
                    p_sigmae.append(p)
        for r in list(add_col_b[p]):
            #bs_sum = bs_sum + tprb[p,771].x
            if tprb[p,771].x > D_p_b(p):
                #print p, r, D_p_b(p)
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

    print row_loop_a + row_loop_b

    if row_loop_a + row_loop_b == 0.:
        row_loop = False
        
    row_list.append(row_loop_a+row_loop_b)  
    
#Get dual variables
#pi = [c.Pi for c in m.getConstrs()]
#
#pi_fe = pi[1880:1880+len(Lf)]
#pi_fb = pi[1880+len(Lf):1880+len(Lf)+len(Lf)]
#pi_b = pi[1880+len(Lf)+len(Lf):1880+len(Lf)+len(Lf)+len(Lb)]
#sigma_e = pi[1880+len(Lf)+len(Lf)+len(Lb):1880+len(Lf)+len(Lf)+len(Lb)+len(p_sigmae)]
#sigma_b = pi[1880+len(Lf)+len(Lf)+len(Lb)+len(p_sigmae):1880+len(Lf)+len(Lf)+len(Lb)+len(p_sigmae)+len(p_sigmab)]

    
t_endbb = time.time()
print "Generating results"   



fres = []
yres = []
teres = []
tbres = []
A340 = []
B737 = []

for v in m.getVars():
    if 'f' == str(v.varName[0]) and v.x > 0:
        fres.append([v.varName, v.x])
    if 'f' == str(v.varName[0]) and '1' == str(v.varName[-2]) and v.x > 0:
        A340.append([v.varName, v.x])
    if 'f' == str(v.varName[0]) and ('2' == str(v.varName[-2]) or '3' == str(v.varName[-2])) and v.x > 0:
        B737.append([v.varName, v.x])    
    if 'y' == str(v.varName[0]) and v.x > 0:
        yres.append([v.varName, v.x])        
#    if 't' == str(v.varName[0]) and 'e' == str(v.varName[-2]) and v.x > 0:
#        teres.append([v.varName, v.x])
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

with open('A340_flights.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(A340)
    
with open('B737_flights.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(B737)

with open('RES_ec_reallocation.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(teres)     

with open('RES_bus_reallocation.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(tbres)
    
with open('Deliv.csv', 'wb') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows([obj_list, col_list, row_list])
    
   

print 'final obj:', m.objVal
print 'runtime:', (t_endbb-t_start)
print 'iterations:', iters
print '#fik:', len(fres)
print '#yak:', len(yres)
print '#tpre:', len(teres)
print '#tprb:', len(tbres)
print 'columns:', cols
print 'rows:', rows
