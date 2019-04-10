import os
import optparse
import sys

from Agent import *
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
    options, args = opt_parser.parse_args()
    return options


class Program:

    def __init__(self):
        # Create random agents
        self.rand_agents = []

        # Create dummy agents
        self.dummy_agents = []

        # Create our agents
        self.our_agents = []

        # Initialize the QLearning unit
        self.qlu = QLearningUnit()

    def create_rand_agents(self, number):
        """ Create a list of agents of the given type. """
        for i in range(number):
            self.rand_agents.append(RandomAgent('rd' + str(i)))

    def run(self):
        """ Run the main execution. """
        end = False
        pop = 100
        nb_step = 500

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

        # Traci starts sumo as a subprocess and then this script connects and runs
        traci.start([sumoBinary, "-c", "map.sumocfg",
                     "--tripinfo-output", "data.xml"])
        
        # Create agents
        self.create_rand_agents(pop)

        traci.simulationStep()

        # Main loop
        for i in range(nb_step):
            traci.simulationStep()
        
        traci.close()
        sys.stdout.flush()
        
        data = DataParser("data.xml")


if __name__ == "__main__":
    p = Program()

    p.run()
