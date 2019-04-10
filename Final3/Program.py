
from Agent import Agent
from DataParser import DataParser
from QLearningUnit import QLearningUnit

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


if __name__ == "__main__":
    p = Program()