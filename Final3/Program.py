import os
import optparse
import sys

from Agent import *
from OurAgent import OurAgent
from DataParser import DataParser
from QLearningUnit import QLearningUnit

# we need to import some python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
import traci


def get_options():
    """ Get options given in the command line. """
    opt_parser = optparse.OptionParser()
    opt_parser.add_option("--nogui", action="store_true",
                          default=False, help="run the commandline version of sumo")
    opt_parser.add_option("-n", type="int", dest="nb_step")
    opt_parser.add_option("--loadqt", action="store_true", default=False)
    options, args = opt_parser.parse_args()
    return options


class Program:

    def __init__(self):
        # Create random agents
        self.rand_agents = dict()

        # Create dummy agents
        self.dummy_agents = dict()

        # Create our agents
        self.our_agents = dict()

        # Initialize the QLearning unit
        self.qlu = QLearningUnit()

    def create_rand_agents(self, number):
        """ Create a list of agents of the given type. """
        for i in range(number):
            self.rand_agents[Agent.ID] = RandomAgent('rd')

    def maintain_rand_agents(self):
        arrived = traci.simulation.getArrivedIDList()

        for a in arrived:
            if int(a) in self.rand_agents:
                del self.rand_agents[int(a)]
                self.rand_agents[Agent.ID] = RandomAgent('rd')

    def control_agents(self):
        """ Controls our agents. """
        for a in self.our_agents.values():
            a.update_edge()

            # If we are on a new edge
            if a.ChangeEdge:
                # If we've already taken an action
                if a.action != -1:
                    # Judge this action
                    reward = a.curr_state[3 + a.action]

                    # Check if we are at destination
                    if a.isArrived():
                        reward += 100

                    a.judge_action(reward)
                else:
                    a.curr_state = a.find_state()

                a.get_action()

                a.ChangeEdge = False

    def run(self):
        """ Run the main execution. """
        end = False
        pop = 100
        nb_step = 1000

        # Get options
        options = get_options()

        # Get SUMO binary
        if options.nogui:
            sumoBinary = checkBinary('sumo')
        else:
            sumoBinary = checkBinary('sumo-gui')

        # Get number of step
        if (options.nb_step is not None):
            nb_step = options.nb_step

        # Load the Qtable if wanted
        if options.loadqt:
            self.qlu.load_q_table()

        # Traci starts sumo as a subprocess and then this script connects and runs
        traci.start([sumoBinary, "-c", "map.sumocfg",
                     "--tripinfo-output", "data.xml"])
        
        # Create agents
        self.create_rand_agents(pop)

        traci.simulationStep()

        # Main loop
        for i in range(nb_step):
            traci.simulationStep()

            self.maintain_rand_agents()

            if i > 99:
                if ((i - 100) % 14 == 0):
                    # Create a Agent
                    self.our_agents[Agent.ID] = OurAgent('e', self.qlu)
                elif ((i - 100) % 7 == 0):
                    # Create a dummy
                    self.dummy_agents[Agent.ID] = InterestingAgent('e')
            
            self.control_agents()                    
        
        traci.close()
        sys.stdout.flush()
        
        data_dum = DataParser("data.xml", list(self.dummy_agents.keys()))
        data_our = DataParser("data.xml", list(self.our_agents.keys()))


if __name__ == "__main__":
    p = Program()

    p.run()
