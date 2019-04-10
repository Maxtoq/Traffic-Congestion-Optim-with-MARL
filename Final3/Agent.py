"""
DEST 0 = E18
DEST 1 = -E7
DEST 2 = -E0

"""

from mapinfo import *

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
	MAP = MapInfo()
	
	def __init__(self, id):
		self.map = Map() # del
	
		self.id = str(id)
		self.type = "car" # del
		self.edge = ""
		self.ChangeEdge = False
		
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
	
	def give_my_edge(self):
		traci.vehicle.getRouteIndex(self.id)
	def get_Edge_Vehicle_At(self, id):
		return get_Edge_ID(traci.vehicle.getRouteIndex(id))
		
	def update_edge(self):
		if(self.edge == ""):
			self.edge = traci.vehicle.getRoadID(str(self.id))
			
		if(self.edge != traci.vehicle.getRoadID(str(self.id))):
			self.edge = traci.vehicle.getRoadID(str(self.id))
			self.ChangeEdge = True
	
	def get_Edge_ID(self, node):
		ret = 0
		
		#0 pour positif
		#1 pour negatif
		sign = 0
		
		print("---  " + node + "  ---")
		if(node[0] == '-'):
			print("...  " + node[2: len(node)] + "  ...")
			ret =  int(node[2: len(node)])
			sign = 1
		else:
			print("...  " + node[1: len(node)] + "  ...")
			ret =  int(node[1: len(node)])
			sign = 0
			
		return ret, sign
		
	def give_n(self, edge):
		ret = 0
		if(edge == 0 or edge == 1):
			ret = 2
		elif(edge == 7 or edge == 24 or edge == 8):
			ret = 1
		elif(edge == 16 or edge == 17 or edge == 18):
			ret = 0
			
		return ret
		
		
	def Options_Available(self, edge):
		
		#Renvoie les options de direction et l edge associe
		#VERIFIER QUE LE EDGE EST UN NOM COMPREHENSIBLE
		return MAP.info[edge]
	
	def Pop_at_Next(self, edge):
			#renvoie un tuple avec la population des prochains edges
		
		opt = Options_Available(edge) #renvoie ( id_edge ou "", , )
		ret = (-1, -1, -1)
		
		for it in opt:
			if(it == ""):
				print("-")
			else:
				it = traci.edge.getLastStepVehicleNumber(it)
		
		return ret
		
	def leftest(self, triple):
	#renvoie l'edge le plus a gauche - ON SUPPOSE SANS CUL DE SAC
		ret = ""
		if(triple[0] != ""):
			ret = triple[0]
		else:
			i = 0
			rightest = opt[i]
			while(rightest == ""):
				if(i<3):
					i += 1
				if(opt[i] != ""):
					rightest = opt[i]
		
		
	
	def turn_right(self):# """ ATTENTION IL NE CREE QU'UN CHEMIN PARTIEL  """
		opt = Options_Available(self.edge)
		i = 0
		rightest = opt[i]
		while(rightest != ""):
			if(i<3):
				i += 1
			if(opt[i] != ""):
				rightest = opt[i]
			
		if(rightest == ""):
			return ("WHUT?")
		else:
			opt_1 = Options_Available(leftest(opt))
			
			
	#def turn_stright(self):
	
	#def turn_left(self):
	

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
		bin = 0
		
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
		
		self.start_n, bin = self.get_Edge_ID(start)
		self.end_n, bin = self.get_Edge_ID(end)
		
		self.start_n = self.give_n(self.start_n)
		self.end_n = self.give_n(self.start_n)

		
	def get_path(self):
		""" Get the path to complete the route with SUMO's algo. """
		return 1
