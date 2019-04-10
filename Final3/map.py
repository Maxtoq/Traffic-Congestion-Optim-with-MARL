import os
import sys
import optparse
from random import randint

import constants as tc
import numpy as np
from Agent import *
from DataParser import DataParser

"""Quelques variable globales pour le fun"""
junctionID = 'gneJ33' #pour le module de stats
N = 5 #population de la simu
POP = 0
R = 0 #list of roads3

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
		
		if id_list is not None:
			if(i < 5):
				AgentList.insert(i , InterestingAgent(i, 1))
				Study_ID.insert(i, i)
			else : 
				AgentList.insert(i , RandomAgent(i))
		
		else : 
			AgentList.insert(i , RandomAgent(i))
	i += 1
		
		
def MaintainAgents(AgentList, Study_ID = None):
	Arrived = traci.simulation.getArrivedIDList()
	print("ARRIVED : " + str(Arrived))
	
	global POP
	
	if (len(Arrived) > 0):#des agents disparus
		for d in Arrived:
			if(int(d) in Study_ID)
				AgentList.insert(int(d), InterestingAgent(int(d)))
			else : 
				AgentList.insert(int(d), RandomAgent(int(d)))
			
			
	"""i = traci.simulation.getMinExpectedNumber()
	if(i != (N-1)):
		while(i < N):
			AgentList.insert(i , RandomAgent(i))
			i += 1
			POP += 1"""
	


def Interact(AgentList):

	print(traci.vehicle.getIDList())
	print("Select a vehicle (by id) \n")
	v = input()

	Ag = AgentList[v]
	v = raw_input("give edge")
	print(Ag.map.get_Pnd_At_Edge(v))
	
	#v=raw_input("New destination ?")
	#Ag.set_Dest(v)
	
	
	

# contains TraCI control loop
def run(Study_ID):

	#Initialisation pre step 1
	go = 1
	step = 0
	
	global POP
	
	traci.simulationStep()
	#Initialisation post step 1
	
	AgentList = list()
	CreateAgents(N, AgentList, Study_ID)
	POP = N
	
	while POP > 0:
		traci.simulationStep()
		POP  -= traci.simulation.getArrivedNumber()
		MaintainAgents(AgentList, Study_ID)
		
		print(str(step) + " - pop : " + str(POP))

		#User interaction
		if (step % 100 == 0 ):
			"""global N 
			N += 1"""
			#Interact(AgentList)
			#go = 0
			
			
		###Data Recovery
		"""
		scResults = traci.junction.getContextSubscriptionResults(junctionID)
		print(traci.junction.getContextSubscriptionResults(junctionID))
		
		halting = 0
		if scResults:
			relSpeeds = [d[tc.VAR_SPEED] / d[tc.VAR_ALLOWED_SPEED] for d in scResults.values()]
			# compute values corresponding to summary-output
			running = len(relSpeeds)
			halting = len([1 for d in scResults.values() if d[tc.VAR_SPEED] < 0.1])
			meanSpeedRelative = sum(relSpeeds) / running
			timeLoss = (1 - meanSpeedRelative) * running * stepLength
			print(traci.simulation.getTime(), timeLoss, halting)
		
		"""

		step += 1
	
	traci.close()
	sys.stdout.flush()
	
	return Study_ID


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
    Study_ID = run(Study_ID)
    data = DataParser("data.xml", Study_ID)

