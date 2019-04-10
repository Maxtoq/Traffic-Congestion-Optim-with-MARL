import numpy as np
import random as rd
import warnings
warnings.filterwarnings('ignore')


def discr_pop(pop):
    """ Discretise a population value. """
    elif (pop < 11):
        return 0
    elif (pop < 21):
        return 1
    elif (pop < 36):
        return 2
    else:
        return 3


class QLearningUnit:

    # STATES
    # Number of edges
    NB_EDGES = 29
    # Number of destination edges
    NB_DEST_EDGE = 3
    # Number of discrete values for the 'number of car in one edge'
    NB_POP_IN_EDGE = 4

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
                                * (self.NB_POP_IN_EDGE ** 3), 3))
        
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
        return (state[0] * 2 * self.NB_DEST_EDGE * (self.NB_POP_IN_EDGE ** 3) 
                + state[1] * self.NB_DEST_EDGE * (self.NB_POP_IN_EDGE ** 3)
                + state[2] * (self.NB_POP_IN_EDGE ** 3) 
                + state[3] * (self.NB_POP_IN_EDGE ** 2)
                + state[4] * self.NB_POP_IN_EDGE
                + state[5])

    def update_q_value(self, state, action, new_q):
        """ Updates a given Q value. """
        self.qtable[self.get_state_id(state), action] += new_q

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

    def choose_action(self, state):
        action = -1

        use_state = (state[0], state[1], state[2], discr_pop(state[3]), 
                     discr_pop(state[4]), discr_pop(state[5]))

        while True:
            if rd.random() > self.eps:
                # Do exploitation
                action = self.exploitation(use_state)
            else:
                # Do exploration
                action = self.exploration()

            # Check if the action is right
            if state[3 + action] == -1:
                # Give very bad reward to impossible action and get new action
                self.update_q_value(use_state, action, -1000)
            else:
                break

        # Decay exploration rate
        if self.eps > self.min_eps:
            self.eps -= self.decay_eps

        return action

    def compute_bellman(self, action, reward, curr_state, new_state):
        """ Update a Q value using Bellman's equation. """
        # Get the usable states
        use_curr_state = (curr_state[0], curr_state[1], curr_state[2], discr_pop(curr_state[3]),
                          discr_pop(curr_state[4]), discr_pop(curr_state[5]))
        use_new_state = (new_state[0], new_state[1], new_state[2], discr_pop(new_state[3]),
                     discr_pop(new_state[4]), discr_pop(new_state[5]))

        # Compute Bellman's equation and update the Q value
        new_q = self.lr * (reward + self.dr * np.amax(self.qtable[self.get_state_id(use_new_state)]) 
                 - self.qtable[self.get_state_id(use_curr_state), action])
        self.update_q_value(use_curr_state, action, new_q)
