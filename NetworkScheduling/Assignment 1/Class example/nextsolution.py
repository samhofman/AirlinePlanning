# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 10:58:22 2019

@author: woute
"""

#from initial_solution import *
from tableaux import *
from initial_solution import slack_row



def slack_row_add(a): #Make function that, for every row, decides whether a slack variable is used
    for row in slack_row: #For all the values of the slack_row matrix
        if row == a: #Check if that value is equal to the row number currently used in Gurobi
            slack_row_add = 1. #If that's true, assign value 1, and use a slack variable in Gurobi
        else:
            slack_row_add = 0. #If that's not true, assign value 0, and do not use a slack variable in Gurobi
    return slack_row_add
        


z = 1

while z <2:
    

    m = grb.Model('MaxExample')
    
    
    # DECISION VARIABLES
    fraction     = {}    #f_k,p
    slack2        = {}    #s_i,j
    
    ### CREATE DECISION VARIABLES ###########################################################################################
    for k in range(len(commodities)):
        for p in range(len(SP[k])):
                fraction[k,p] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                            name="f_%s,%s"%(k,p))
    
    for a in range(len(arcs)):
                slack2[a] = m.addVar(vtype=GRB.CONTINUOUS, lb=0,
                            name="s_%s"%(a))
    
    m.update()

    

    
    ##### OBJECTIVE FUNCTION #################################################################################################
    
    obj = grb.quicksum(grb.quicksum(d(k)*cp(k,p)*fraction[k,p] for p in range(len(delta_sp[k][p]))) for k in range(len(commodities))) + 1000 * grb.quicksum(slack_row_add(a) * slack2[a] for a in range(len(arcs)))
    
       
    
    m.setObjective(obj,GRB.MINIMIZE) #fill in obj instead of m.getObjective
    
    print "Objective function created."
    
    
    ##### CONSTRAINTS ########################################################################################################
    
    ### 1 ################################################################
    print "Constraint 1 loading"
    
    for i in range(len(arcs)):
        m.addConstr(grb.quicksum(grb.quicksum(d(k)*fraction[k,p]*delta(k,p,i) for p in range(len(delta_sp[k][p]))) for k in range(len(commodities))) - slack_row_add(i) * slack2[i]
        ,
                                GRB.LESS_EQUAL,
                                u(i))
    
    ### 2 ################################################################
    print "Constraint 2 loading"
    
    for k in range(len(commodities)):
        m.addConstr(grb.quicksum(fraction[k,p] for p in range(len(delta_sp[k][p]))),
                                GRB.EQUAL,
                                1)
     
    #for a in range(len(arcs)):
    #    m.addConstr(slack[a], 
    #                GRB.EQUAL, 
    #                max{0,grb.quicksum(grb.quicksum(d(k)*fraction[k,p]*delta(k,p,arcs[i][1],arcs[i][2]) for p in range(len(P[k]))) for k in range(len(commodities))) - u(a)} )
        
    
    
    m.write("model.lp")
    
    m.optimize()
    
    pi = [c.Pi for c in m.getConstrs()]
    
    sigma = pi[len(arcs):(len(arcs)+len(commodities))]
    pi = pi[:len(arcs)]
#    pi = [0,0,0,-6,0,-6,0]
#    sigma = [165, 60, 130, 55]
    
    
    c_sigma.append([sigma])
    c_pi.append([pi])
        
    for v in m.getVars():
        if v.x > 0:
            print (v.varName, v.x)    
    print ('Obj:', m.objVal) 
    
    
    G = nx.DiGraph()
    
    for i in range(len(arcs)):
        G.add_edge(arcs[i][1], arcs[i][2], weight = arcs[i][3]-pi[i])
    
    SPnew = []
    #P = []        #P[k][p][n] k commodity, p path number, n node
    
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
                    elif SPnew[k][p][n] == arcs[a][2] and SPnew[k][p][n+1] == arcs[a][1]:
                        delta_spnew[k][a][p] = 1.
             
#    z = 0.    
#    for k in range(len(commodities)):
#        if cppi(k) < sigma[k]/d(k):
#            for p in range(len(SP[k])):
#                if SPnew[k][0] != SP[k][p]:
#                    z = z + 1
#                    SP[k].append(SPnew[k][-1])
#                    delta_sp[k] = np.hstack((delta_sp[k],delta_spnew[k]))
#                    break
#                else: 
#                    break
                
    z = 0    
    for k in range(len(commodities)):
        print cppi(k), sigma[k]/d(k)
        if cppi(k) < sigma[k]/d(k):
            it = 0
            for p in range(len(SP[k])):
                if SPnew[k][0] == SP[k][p]:
                    it = it + 1
            if it == 0:        
                SP[k].append(SPnew[k][0])
                delta_sp[k] = np.hstack((delta_sp[k],delta_spnew[k]))
                print SP[k]
                z = z + 1            

            
           
            
            
            