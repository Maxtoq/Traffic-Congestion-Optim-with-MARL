from Agent import InterestingAgent


class OurAgent(InterestingAgent):

	def __init__(self, id, qlu):
		InterestingAgent.__init__(self, id)

		# Add access to the QLearning Unit
		self.qlu = qlu

	def find_state(self):
		""" Translate data from SUMO to a state usable by the QLU. """
		return 1
