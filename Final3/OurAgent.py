import traci

from Agent import InterestingAgent


class OurAgent(InterestingAgent):

	def __init__(self, id, qlu):
		InterestingAgent.__init__(self, id)

		# Add access to the QLearning Unit
		self.qlu = qlu

        # Current state
        self.curr_state = None

        # Action to take
        self.action = -1

	def find_state(self):
		""" Translate data from SUMO to a state usable by the QLU. """
        # Get the edge where are
		edge = self.get_Edge_At()

        # Get the population at the next edges
        pop_next_edges = self.get_pop_next_edges()

        return (edge[0], edge[1], self.end_n, pop_next_edges[0], 
                           pop_next_edges[1], pop_next_edges[2])

    def get_action(self):
        """ Get an action from the QLU. """
        self.action = self.qlu.choose_action(self.curr_state)

    def judge_action(self):
        """ Get new state and update q value with the Bellman's equation. """
        # Get the new state
        new_state = self.find_state()

        # Update the Q value
        self.qlu.compute_bellman(self.action, self.curr_state, new_state)

        # Update state
        self.curr_state = new_state

