import os
import sys
import random as rd
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
		self.map = Map() # del
	
		self.id = str(id)
		self.type = "car" # del
		
	#GETTERSs
	#def get_Dest(self):
	#	return traci.vehicle.getRoute(str(self.id))
		
	#def get_Vitesse(self):
	#	return traci.vehicle.getRoute(str(self.id))
		
	#SETTERS
	def set_Dest(self, dest):
		#print(type(traci.simulation.findRoute(traci.vehicle.getRoadID(str(self.id)), dest, "car")))
		traci.vehicle.setRoute(str(self.id), traci.simulation.findRoute(traci.vehicle.getRoadID(str(self.id)), dest, "car").edges)

	def give_pop_at_egde_Oriente(self, name):
		return getLastStepVehicleNumber(name)
	
	def give_pop_at_egde(self, name):
		opposite = -int(name)
		
		opposite = str(opposite)
		
		return getLastStepVehicleNumber(name) + getLastStepVehicleNumber(opposite)
	

class RandomAgent(Agent):
	""" Agent with a random route. """

	def __init__(self, id):
		Agent.__init__(self, id)

		self.set_random_route()

	def set_random_route(self):
		""" Find a valid random route for the agent. """
		start_edge = 0
		dest_edge = 0

		while ("ON A PAS UNE ROUTE VALIDE"):
			while (start_edge == dest_edge):
				start_edge = rd.randint(0, traci.edge.getIDCount()-1)
				dest_edge = rd.randint(0, traci.edge.getIDCount()-1)

			EdgeL = traci.edge.getIDList()

			self.pos = EdgeL[start_edge]
			self.dest = EdgeL[dest_edge]

			self.route = traci.simulation.findRoute(self.pos, self.dest, self.type)
			self.Nodes = traci.simulation.findRoute(
			    self.pos, self.dest, self.type).edges

			if (len(self.Nodes) > 3):
				print("out")
				break
			else:
				start_edge = 0
				dest_edge = 0

		traci.route.add("rd" + str(Agent.ROAD_ID), self.Nodes)
		traci.vehicle.add(str(self.id), "rd"+str(Agent.ROAD_ID), str(self.type))

		#c = np.random.normal(0.5, 0.1)
		#traci.vehicle.set
		Agent.ROAD_ID += 1


class InterestingAgent(Agent):

	def __init__(self, id):
		Agent.__init__(self, id)

		# Start and end node
		self.start_n = -1
		self.end_n = -1

		self.find_interesting_route()

	def find_interesting_route(self):
		""" Find an interesting route. """
		# self.start_n = rd.randint(0, 2)
		# self.end_n = self.start_n

		# while (self.start_n == self.end_n):
			# self.end_n = rd.randint(0, 2)
			
		StartE = ["E0", "-E18",  "-E7"]
		EndE = ["-E0","E1", "-E24", "-E7", "-E17", "E18"]
		
		start = rd.randint(0, 2)
		if(start == 0):
			end = rd.randint(2, 5)
			start = StartE[start]
			end = EndE[end]
		elif(start == 1):
			end = rd.randint(0, 3)
			start = StartE[start]
			end = EndE[end]
		elif(start == 2):
			end = 2
			while(end == 2 or end == 3):
				end = rd.randint(0, 5)
				start = StartE[start]
				end = EndE[end]

		self.route = traci.simulation.findRoute(start, end, self.type)
		self.Nodes = traci.simulation.findRoute(start, end, self.type).edges

		traci.route.add("rd" + str(Agent.ROAD_ID), self.Nodes)
		traci.vehicle.add(str(self.id), "rd"+str(Agent.ROAD_ID), str(self.type))

		Agent.ROAD_ID += 1
		
		self.start_n = int(start)
		self.end_n = int(end)

	def get_path(self):
		""" Get the path to complete the route with SUMO's algo. """
		return 1
