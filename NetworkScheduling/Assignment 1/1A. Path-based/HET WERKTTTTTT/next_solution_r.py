# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 16:32:27 2019

@author: woute
"""

from tableaux_r import *
import openpyxl as xl
from initial_solution_r import pi, sigma, c_pi, c_sigma, slack_row, end_init, start_init

start_next = time.time()

GRB = grb.GRB


### CPPI ###
def cppi(k):
    cp = 0.
    for a in range(len(arcs)):
        cp = cp + delta_spnew[k][a][0] * (arcs[a][3] - pi[a])
    return cp    

        


z = 1.

while z > 0.5:
    
### NEW GRAPH WITH UPDATED WEIGHTS ###    
    G = nx.DiGraph()

    for i in range(len(arcs)):
        G.add_edge(arcs[i][1], arcs[i][2], weight = arcs[i][3]-pi[i])
        
    SPnew = []
    for i in range(len(commodities)):
        SPnew.append([[p for p in nx.dijkstra_path(G, source = commodities[i][1], target = commodities[i][2] )]])
    
    
    delta_spnew= {}    #delta[k][a][p]    
    for k in range(len(commodities)):
        delta_spnew[k] = np.zeros((len(arcs),1))    
        
    
    for k in range(len(commodities)):
        for a in range(len(arcs)):
            for p in range(len(SPnew[k])):
                for n in range(len(SPnew[k][p])-1):
                    if SPnew[k][p][n] == arcs[a][1] and SPnew[k][p][n+1] == arcs[a][2]:
                        delta_spnew[k][a][p] = 1.
#                    elif SPnew[k][p][n] == arcs[a][2] and SPnew[k][p][n+1] == arcs[a][1]:
#                        delta_spnew[k][a][p] = 1.    
                        
    
    z = 0.       
    for k in range(len(commodities)):
        if cppi(k) < sigma[k]/d(k):
            it = 0.
            
            for p in range(len(SP[k])):
                if SPnew[k][0] == SP[k][p]:
                    it = it + 1
            if it == 0:        
                SP[k].append(SPnew[k][0])
                delta_sp[k] = np.hstack((delta_sp[k],delta_spnew[k]))
                z = z + 1
    print "Columns added:", z
    if z == 0.:
        
        for v in m.getVars():
            if v.x > 0:
                print (v.varName, v.x)    
        print ('Obj:', m.objVal)
        break
   
                
    m = grb.Model('MaxExample')
    
    
    # DECISION VARIABLES
    fraction     = {}    #f_k,p
    slack        = {}    #s_i,j
    
    ### CREATE DECISION VARIABLES ###########################################################################################
    for k in range(len(commodities)):
        for p in range(len(SP[k])):
                fraction[k,p] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                            name="f_%s,%s"%(k,p))
    
    for a in range(len(arcs)):
                slack[a] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                            name="s_%s"%(a))
    
    m.update()

    

    
    ##### OBJECTIVE FUNCTION #################################################################################################
    
    obj = grb.quicksum(grb.quicksum(d(k)*cp(k,p)*fraction[k,p] for p in range(len(SP[k]))) for k in range(len(commodities))) + grb.quicksum( 1000 * slack_row[a] * slack[a] for a in range(len(arcs)))
    
       
    
    m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective
    
    print "Objective function created."
    
    
    ##### CONSTRAINTS ########################################################################################################
    
    ### 1 ################################################################
    print "Constraint 1 loading"
    
    for a in range(len(arcs)):
        m.addConstr(grb.quicksum(grb.quicksum(d(k)*fraction[k,p]*delta_sp[k][a][p] for p in range(len(SP[k]))) for k in range(len(commodities))) - slack_row[a] *  slack[a]
        ,
                                GRB.LESS_EQUAL,
                                u(a))
    
    ### 2 ################################################################
    print "Constraint 2 loading"
    
    for k in range(len(commodities)):
        m.addConstr(grb.quicksum(fraction[k,p] for p in range(len(SP[k]))),
                                GRB.EQUAL,
                                1)
     
    
    m.update()
    
    m.write("model.lp")
    
    
    m.optimize()

#    for v in m.getVars():
#        if v.x > 0:
#            print (v.varName, v.x)    
#    print ('Obj:', m.objVal)

    pi = [c.Pi for c in m.getConstrs()]
    
    sigma = pi[len(arcs):(len(arcs)+len(commodities))]
    pi = pi[:len(arcs)]
    
    c_sigma.append([sigma])
    c_pi.append([pi])


end_next = time.time()

print "Tableaux time:", end_tab-start_tab
print "Initial run time:", end_init-start_init
print "Iterations run time:", end_next-start_next
print "Total run time:", end_tab-start_tab+end_init-start_init+end_next-start_next


import pandas as pd

wb2 = xl.load_workbook("InputLetters.xlsx", read_only=True)
S3 = wb2['Arcs']
codes = np.array([[i.value for i in j] for j in S3['A2':'A17']])
codes_l = np.array([[i.value for i in j] for j in S3['B2':'B17']])

SP_let = SP


for k in range(len(commodities)):
    for p in range(len(SP[k])):
        for n in range(len(SP[k][p])):
            for a in range(16):
                if SP[k][p][n] == codes[a][0]:
                    SP_let[k][p][n] = str(codes_l[a][0])

#for k in range(len(commodities)):
#    for p in range(len(SP[k])):                    
#        if fraction[k,p].x > 0.:
#            print k, fraction[k,p].x, SP_let[k][p]


        
    
        
        
    
    
    
    
    
    
    
    