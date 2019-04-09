import os
import sys
import optparse
from random import randint

import constants as tc
import numpy as np

"""Quelques variable globales pour le fun"""
junctionID = 'gneJ33' #pour le module de stats
N = 5 #population de la simu
POP = 0
R = 0 #list of roads


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
	
class Information:
	def _init_(self):
		self.calculatedWaitingTime = -1
		self.realWaitingTime = -1
		self.calculatedDistanceDriven = -1
		self.realDistanceDriven= -1
		self.sigma = -1
		
	def _init_(self, WT, DD, sigma):
		self.calculatedWaitingTime = WT
		self.realWaitingTime = -1
		self.calculatedDistanceDriven = DD
		self.realDistanceDriven= -1
		self.sigma = sigma
		
	def get_CWT():
		return self.calculatedWaitingTime
	def get_RWT():
		return self.realWaitingTime
	def get_CDD():
		return self.calculatedDistanceDriven
	def get_RDD():
		return self.realDistanceDriven
	def get_sigma():
		return self.sigma
		
	def set_CWT(self, p):
		self.calculatedWaitingTime = p
	def set_RWT(self, p):
		self.realWaitingTime = p
	def set_CDD(self, p):
		self.calculatedDistanceDriven = p
	def set_RDD(self, p):
		self.realDistanceDriven = p
	def set_sigma(self, p):
		self.sigma = p
		
		
class Map:
	def __init__(self):
		self.Graph = traci.edge.getIDList()
		self.Ponderation = np.empty(len(self.Graph), dtype=int)#traci.edge.getIDList()
		for i in range(len(self.Ponderation)):
			self.Ponderation[i]= 0	
		
		
	def set_Pnd_At(self, id, value):
		self.Ponderation[id] = value
	def get_Pnd_At(self, id):
		return self.Ponderation[id]
	def get_Size(self):
		return len(self.Graph)
	def get_Pnd_At_Edge(self, name):
		return self.Ponderation[self.Graph.index(name)]
		

class Agent:
	
	def __init__(self, id):
	
		self.info = Information()
		self.map = Map()
	
		"""Constructeur"""
		self.id = str(id)
		self.type = "car"

		"""self.vitesse = 50
		self.acceleration = 0"""
		
		al = 0
		be = 0
		 
		global R
		
		while("ON A PAS UNE ROUTE VALIDE"):
			while(al == be):
				al = randint(0, traci.edge.getIDCount()-1)
				be = randint(0, traci.edge.getIDCount()-1)
				
				
			EdgeL = traci.edge.getIDList()

			"""print("EdgeL = " + str(len(EdgeL)))	
			print("a = " + str(al))
			print("beta = " + str(be))"""
			
			self.pos = EdgeL[int(al)]
			self.dest = EdgeL[int(be)]
			
			self.route = traci.simulation.findRoute(self.pos, self.dest, self.type)
			self.Nodes = traci.simulation.findRoute(self.pos, self.dest, self.type).edges
			
			"""print("START : "+ str(id))
			print(self.route)
			print(self.route.edges)
			print(self.type)"""
			
			if(len(self.Nodes)> 4 ):
				print("out")
				break
			else: 
				al = 0
				be = 0
				
		traci.route.add("rd"+str(R), self.Nodes)
		traci.vehicle.add(str(self.id), "rd"+str(R), str(self.type)) 
		
		#c = np.random.normal(0.5, 0.1)
		#traci.vehicle.set
		R += 1
		
		
	#GETTERSs
	def get_Dest(self):
		return traci.vehicle.getRoute(str(self.id))
		
	def get_Vitesse(self):
		return traci.vehicle.getRoute(str(self.id))
		
	#SETTERS
	def set_Dest(self, dest):
		#print(type(traci.simulation.findRoute(traci.vehicle.getRoadID(str(self.id)), dest, "car")))
		traci.vehicle.setRoute(str(self.id),  traci.simulation.findRoute(traci.vehicle.getRoadID(str(self.id)), dest, "car").edges)
		
	def give_pop_at_egde_Oriente(self, name):
		return getLastStepVehicleNumber(name)
	
	def give_pop_at_egde(self, name):
		opposite = -int(name)
		
		opposite = str(opposite)
		
		return getLastStepVehicleNumber(name) + getLastStepVehicleNumber(opposite)
	
	
			

def CreateAgents(AgentList):
	i = 0
		
	while i < N:
		AgentList.insert(i , Agent(i))
		i += 1
		
		
def MaintainAgents(AgentList):
	Arrived = traci.simulation.getArrivedIDList()
	print("ARRIVED : " + str(Arrived))
	
	global POP
	
	if (len(Arrived) > 0):
		for d in Arrived:
			AgentList.insert(int(d), Agent(int(d)))
			
	i = traci.simulation.getMinExpectedNumber()
	if(i != (N-1)):
		while(i < N):
			AgentList.insert(i , Agent(i))
			i += 1
			POP += 1
	


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
def run():

	#Initialisation pre step 1
	go = 1
	step = 0
	
	global POP
	
	#init Data_Recovery
	"""
	traci.vehicle.subscribeContext(junctionID, tc.CMD_GET_VEHICLE_VARIABLE, 1000000, [tc.VAR_SPEED, tc.VAR_ALLOWED_SPEED])
	stepLength = traci.simulation.getDeltaT()
	"""
	
	traci.simulationStep()
	#Initialisation post step 1
	
	AgentList = list()
	CreateAgents(AgentList)
	POP = N
	
	while POP > 0:
		traci.simulationStep()
		POP  -= traci.simulation.getArrivedNumber()
		MaintainAgents(AgentList)
		
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
    run()
    execfile("schem.py")

