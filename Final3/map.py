import os
import sys
import optparse
from random import randint

import constants as tc
import numpy as np
from Agent import *
from mapinfo import *
from DataParser import DataParser

"""Quelques variable globales pour le fun"""
junctionID = 'gneJ33' #pour le module de stats
N = 20 #population de la simu
POP = 0
R = 0 #list of roads3
I = 0

Study_ID = list()


# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

	
from sumolib import checkBinary  
import traci

def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = opt_parser.parse_args()
    return options
	

			

def CreateAgents(AgentList, Study_ID = None ):	
	i = 0
	while i < N:
		print("Creating " + str(i))
		if Study_ID is not None:
			if(i < 5):
				AgentList.insert(i , InterestingAgent(i))
				Study_ID.insert(i, i)
				AgentList[i].update_edge()
				i += 1
			else : 
				AgentList.insert(i , RandomAgent(i))
				AgentList[i].update_edge()
				i += 1
		else : 
			AgentList.insert(i , RandomAgent(i))
			AgentList[i].update_edge()
			i += 1
		
	
	return i
		
		
def MaintainAgents(AgentList, I, Study_ID = None):
	Arrived = traci.simulation.getArrivedIDList()
	print("ARRIVED : " + str(Arrived))
	
	global POP
	print("Major I = " + str(I))
	
	if (len(Arrived) > 0):#des agents disparus
		for d in Arrived:
			if(int(d) in Study_ID):
				AgentList.insert(int(d), InterestingAgent(I))
				Study_ID.insert(len(Study_ID), I)
			else : 
				AgentList.insert(int(d), RandomAgent(I))
			POP += 1
			
			I += 1
	
	return I
		

def Interact(AgentList):

	print(traci.vehicle.getIDList())
	print("Select a vehicle (by id) \n")
	v = raw_input()
	if(v != ""):
		Ag = AgentList[int(v)]
		print("Agent : " + str(int(v))) 
		Ag.turn_right()
	
	#v = raw_input("give edge")
	#print(Ag.map.get_Pnd_At_Edge(v))
	#
	#v=raw_input("New destination ?")
	#Ag.set_Dest(v)
	
	
# contains TraCI control loop
def run(Study_ID, I):

	#Initialisation pre step 1
	go = 1
	step = 0
	
	global POP
	
	traci.simulationStep()
	#Initialisation post step 1
	
	AgentList = list()
	I = CreateAgents(AgentList, Study_ID)
	POP = N
	
	while (POP > 0 and step < 1000): #SECONDE CONDITION TEMPORAIRE
		traci.simulationStep()
		POP  -= traci.simulation.getArrivedNumber()
		
		for a in AgentList:
			if(a.id < I-1):
				a.update_edge()
		
		I = MaintainAgents(AgentList, I,  Study_ID)
		
		print(str(step) + " - pop : " + str(POP))

		#User interaction
		if (step % 20 == 0 ):
			"""global N 
			N += 1"""
			Interact(AgentList)
			

		step += 1
	
	
	for it in Study_ID:
		print (str(it) + " - ")
	traci.close()
	sys.stdout.flush()
	
	return Study_ID, I


# main entry point
if __name__ == "__main__":
    options = get_options()

    # check binary
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # traci starts sumo as a subprocess and then this script connects and runs
    traci.start([sumoBinary, "-c", "map.sumocfg" , "--tripinfo-output", "data.xml"])
    Study_ID, I = run(Study_ID, I)
    data = DataParser("data.xml", Study_ID)

