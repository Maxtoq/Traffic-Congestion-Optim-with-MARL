import os
import sys
from random import randint
import numpy as np

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  
import traci


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

	ROAD_ID = 0
	
	def __init__(self, id):
	
		self.map = Map()
	
		self.id = str(id)
		self.type = "car"
		
		al = 0
		be = 0
		
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
		
		traci.route.add("rd" + str(Agent.ROAD_ID), self.Nodes)
		traci.vehicle.add(str(self.id), "rd"+str(Agent.ROAD_ID), str(self.type))
		
		#c = np.random.normal(0.5, 0.1)
		#traci.vehicle.set
		Agent.ROAD_ID += 1
		
		
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
	
	
