# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:35:24 2019

@author: hofma
"""

from Crew_Pairing_Input import *
from math import *
from Crew_Functions import *

#Make list of possible pairing start flights at base for eacht aircraft type
B737_pairings = []

for i in range(len(arc_no_737)):
    if flight_no_737[i][1] == 'AEP':
        B737_pairings.append([arc_no_737[i][0]]) #Each row is new possible starting point
 
#Convert arc numbers to list instead of array
B737_flights = list(arc_no_737.flat) 

##### FOR THE B737 #####

#Check which pairings are valid to add another flight to
index = 0
i = 0
possible_B737_pairings = [] #Add possible pairings to external (out of the loop) list
while index < len(B737_pairings):
    last_destination = flight_destin_737(B737_pairings[i][-1]) #Define last destination of last flight in pairing
    if Pairing_function_737(B737_pairings,i) == (True, True, True): #If the pairing satisfies the requirements
        for u in B737_flights: #Loop over all B737 flights
            if last_destination == flight_origin_737(u): #If the origin of a new possible flight matches the last_destination
                new_pairing = list(B737_pairings[i]) #Make list of current pairing (easier to work with)
                if (u not in new_pairing) is True: #If flight is not in pairing yet
                    new_pairing.append(u) #Append current pairing with new flight
                    new_pairing = [new_pairing] #Make it an array again in order to be able to run it in Pairing_function
                    if Pairing_function_737(new_pairing, 0) == (True, True, True): #If the new pairing satisfies the requirements
                        add_pairing = new_pairing[0] #Define new pairing to be added
                        B737_pairings.append(add_pairing) #Add new pairing to list of B737_pairings
                        possible_B737_pairings.append(add_pairing) #And add it to the external list
            else: #If the origin of a new possible flight does not match the last_destination
               continue #Just move on to next u
        B737_pairings.remove(B737_pairings[i]) #Remove old pairing
    else: #If the pairing does not satisfy the requirements
        i += 1 #Move to next pairing
    index += 1 

#Remove pairings that don't end in base
final_B737_pairings = []
for i in range(len(possible_B737_pairings)):
    if flight_destin_737(possible_B737_pairings[i][-1]) == 'AEP':
        final_B737_pairings.append(possible_B737_pairings[i])

#Check if all flights are flown
#Make list of all flown flights        
flights_flown = []
for j in range(len(final_B737_pairings)):
    for k in final_B737_pairings[j]:
        flights_flown.append(k)

#Then check if B737_flight is present in at least one pairing        
print 'The following flights cannot be added to a feasible pairing:'
for i in B737_flights:
    if i not in flights_flown:
        print i
        B737_flights.remove(i) #remove flights from B737_flights to check if now a feasible set can be formed
        
#Make set of feasible pairings

all_flights = False #To check whether all 737 flights are in the set of pairings
i = 0 #Index of first pairing
maxlen = [] #A list to store the length of the set of pairings found
while all_flights is False:
    check = [] #Set of pairings [[pairing 1], [pairing 2], [etc.]]
    iteration = 0     
    feasible_set = [] #Set of flights in set of pairings [pairing_1_flight_1, pairing_1_flight_2, pairing_2_flight_1, etc.]  (easier to work with)   
    if iteration == 0: #If it's the first iteration, append the set with the current analysed pairing
        check.append(final_B737_pairings[i])
        for k in final_B737_pairings[i]:
            feasible_set.append(k)
        iteration += 1
    for m in range(len(final_B737_pairings)): #Go over all possible pairings
        #If all flights of that pairing are not yet in the feasible set, append that pairing
        if all(final_B737_pairings[m][j] not in feasible_set for j in range(len(final_B737_pairings[m]))) is True: #If True
            check.append(final_B737_pairings[m])
            for k in final_B737_pairings[m]:
                feasible_set.append(k)
        else:
            continue
    #maxlen.append(len(feasible_set))
    i += 1 #Take next pairing of all possible pairings as the first pairing in the feasible set of pairings
    if all(j in feasible_set for j in B737_flights) is True: #If all B737 flights are in the set, stop looping
        all_flights = True
    #If all possible pairings have been taken as first pairing in a possible set, no feasible pairing is found, so stop looping
    if i > len(final_B737_pairings)-1: 
        print 'No feasible set found'
        all_flights = True
    #This has to be done manually. It was found that the max length of a feasible set was 93,\
    #so that was the set where the most flights could be executed
    if len(feasible_set) == 93:
        all_flights = True

#print max(maxlen)

print 'The following flights cannot be flown in the feasible set:'
for i in B737_flights:
    if i not in feasible_set:
        print i
        
#Change list to flight numbers
for i in range(len(check)):
    for j in range(len(check[i])):
        check[i][j] = flight_number_737(check[i][j])


