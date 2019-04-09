import numpy as np
import random as rd
import warnings
warnings.filterwarnings('ignore')

class QLearningUnit:

    # STATES
    # Number of edges
    NB_EDGES = 29
    # Number of destination edges
    NB_DEST_EDGE = 3
    # Number of discrete values for the 'number of car in one edge'
    NB_CARNB_IN_EDGE = 4

    def __init__(self):
        # Q-table, contains all the Q-values for all the (state-action) couples
        # States: - # of the edge
        #         - orientation
        #         - destination node
        #         - nb of cars on edge 1
        #         - nb of cars on edge 2
        #         - nb of cars on edge 3
        # Actions: go left, go straight, go right
        self.qtable = np.zeros((self.NB_EDGES * 2 * self.NB_DEST_EDGE 
                                * (self.NB_CARNB_IN_EDGE ** 3), 3))

        self.actions = []
        self.rewards = []
        
        # Exploration rate
        self.eps = 1
        self.min_eps = 0.1
        self.decay_eps = 0.001
        
        # Learning rate
        self.lr = 0.001
        
        # Discount rate
        self.dr = 0.9

    def get_state_id(self, state):
        """ Returns the id of a state in the Q-table. """
        # state = (# of the edge (0-28), orientation (0-1), destination (0-2), nb of cars on edge 1 (0-3), nb of cars on edge 2 (0-3), nb of cars on edge 3 (0-3))
        return (state[0] * 2 * self.NB_DEST_EDGE * (self.NB_CARNB_IN_EDGE ** 3) 
                + state[1] * self.NB_DEST_EDGE * (self.NB_CARNB_IN_EDGE ** 3)
                + state[2] * (self.NB_CARNB_IN_EDGE ** 3) 
                + state[3] * (self.NB_CARNB_IN_EDGE ** 2)
                + state[4] * self.NB_CARNB_IN_EDGE
                + state[5])

    def update_q_value(self, state, action, reward):
        """ Updates a given Q value with the given reward. """
        self.qtable[self.get_state_id(state), action] += reward

    def exploration(self):
        """ Returns a random choice of action. """
        return rd.randint(0, 2)

    def exploitation(self, state):
        """ Choose the action with the biggest Q-value in the Q-table. """
        # Get the id of the state in the Q-table
        state_id = self.get_state_id(state)

        # Get the biggest Q-value at that state
        qmax = np.amax(self.qtable[state_id])

        # If this is the Q-value for multiple actions, choose randomly between these actions
        count = np.count_nonzero(self.qtable[state_id] == qmax)
        if count > 1:
            rn = rd.randint(1, count + 1)
            act = 0
            for i in range(len(self.qtable[0])):
                if self.qtable[state_id, i] == qmax:
                    act = i
                    rn -= 1
                if rn == 0:
                    break
            return act
        else:
            return np.argmax(self.qtable[state_id])

    def choose_action(self, state, possible_actions):
        action = -1

        while True:
            if rd.random() > self.eps:
                # Do exploitation
                action = self.exploitation(state)
            else:
                # Do exploration
                action = self.exploration()

            # Check if the action is right
            if action in possible_actions:
                break
            else:
                # Give very bad reward to impossible action and get new action
                self.update_q_value(state, action, -1000)
        
        self.actions

        # Decay exploration rate
        if self.eps > self.min_eps:
            self.eps -= self.decay_eps


ql = QLearningUnit()

print(ql.get_state_id((1, 1, 0, 0, 0, 0)))
