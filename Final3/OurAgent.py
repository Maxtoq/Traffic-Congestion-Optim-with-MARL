import traci

from Agent import InterestingAgent


class OurAgent(InterestingAgent):

    def __init__(self, id, qlu):
        InterestingAgent.__init__(self, id)
        self.update_edge()

        # Add access to the QLearning Unit
        self.qlu = qlu

        # Current state
        self.curr_state = None

        # Action to take
        self.action = -1

    def find_state(self):
        """ Translate data from SUMO to a state usable by the QLU. """
        # Get the edge where we are
        edge = self.get_Edge_ID()

        # Get the population at the next edges
        pop_next_edges = self.Pop_at_Next()

        return (edge[0], edge[1], self.end_n, pop_next_edges[0], 
                           pop_next_edges[1], pop_next_edges[2])

    def get_action(self):
        """ Get an action from the QLU. """
        self.action = self.qlu.choose_action(self.curr_state)

        if (self.action == 0):
            self.turn_left()
        elif (self.action == 1):
            self.turn_stright()
        elif (self.action == 2):
            self.turn_right()

    def judge_action(self, reward):
        """ Get new state and update q value with the Bellman's equation. """
        # Get the new state
        new_state = self.find_state()

        # Update the Q value
        self.qlu.compute_bellman(self.action, reward, self.curr_state, new_state)

        # Update state
        self.curr_state = new_state

