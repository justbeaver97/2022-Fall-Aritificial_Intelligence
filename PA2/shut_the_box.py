import random
from itertools import chain, combinations

class State(tuple):
	# A state is defined as a tuple (numbers, dice_summation)
	# Access with the following command:
	# numbers, dice_summation = state
	def __new__(self, numbers_left, dice_summation):
		return tuple.__new__(State, (frozenset(numbers_left), dice_summation))

class Environment:
	def __all_states_and_actions(self):
		all_numbers_left = [[], [1]]
		for i in range(2, self.total_numbers + 1):
			for curr in range(len(all_numbers_left)):
				curr_ = all_numbers_left[curr].copy()
				curr_.append(i)
				all_numbers_left.append(curr_)

		all_dice_summation = list(range(2, 12 + 1))

		states = []
		actions = {}
		
		for number_list in all_numbers_left:
			for dice in all_dice_summation:
				states.append(State(number_list, dice))
				actions[State(number_list, dice)] = []

		for numbers in all_numbers_left:
			all_combinations = chain.from_iterable(combinations(numbers, r) for r in range(len(numbers)+1))
			for combination in all_combinations:
				dice = self.calc_sum(combination)
				if dice>=2 and dice<=12:
					actions[State(numbers, dice)].append(combination)
		
		return states, actions


	def __init__(self):
		self.total_numbers = 9
		self.prob_dist = {i:0 for i in range(2, 12 + 1)}
		for i in range(1, 6 + 1):
			for j in range(1, 6 + 1):
				self.prob_dist[i+j] += 1/6 * 1/6
		self.all_states, self.all_states_actions = self.__all_states_and_actions()

	def available_actions(self, state):
		# Return a list of actions that is allowed in this case
		# Each action is a set of numbers.
		return self.all_states_actions[state]

	def all_transition_next(self, numbers_left, action_taken):
		# Return a list of all possible next steps with their probability.
		# Input: Current numbers and an action (a subset of previous numbers)
		# Each next step is represented in tuple (state, probability of the state)
		# State is a tuple itself - (numbers_left, dice_summation) 
		numbers_left = set(numbers_left)
		for it in action_taken:
			numbers_left.remove(it)
		return [(State(numbers_left, sum_), self.prob_dist[sum_]) for sum_ in self.prob_dist]

	def get_all_states(self):
		# Get a list of all states
		# Each state is a tuple - (numbers_left, dice_summation) 
		return self.all_states

	def calc_sum(self, numbers):
		# Calculate the summation of things in a list/set
		s = 0
		for i in numbers:
			s += i
		return s



class Agent:
	def __init__(self, env):
		self.env = env
		self.all_states = env.get_all_states()
		self.utilities = {state:0 for state in self.all_states}

	def giveup_reward(self, numbers_left):
		# The reward for choosing give up at this state
		c = self.env.total_numbers
		return c*(c+1)//2 - self.env.calc_sum(numbers_left)

	def value_iteration(self):
		max_change = 1e5
		while max_change >= 0.001:
			utilities_pre = self.utilities.copy() # Copy the utility, e.g. U_{t-1}
			max_change = 0 # Measure the maximum change in all states for this iteration - if smaller than 0.001 we stop.
			for state in self.all_states:
				# Complete this part with follwoing functions 
				# self.giveup_reward, self.env.available_actions, self.env.all_transition_next
				available_actions = self.env.available_actions(state)
				if available_actions:
					utility = []
					for available_action in available_actions:
						tmp, state_s_prime_list = 0, self.env.all_transition_next(state[0], available_action)
						for state_s_prime in state_s_prime_list:
							tmp += state_s_prime[1] * (0 + utilities_pre[state_s_prime[0]])
							utility.append(tmp)
						self.utilities[state] = max(utility)
				else:
					self.utilities[state] = self.giveup_reward(state[0])
				max_change = max(abs(self.utilities[state] - utilities_pre[state]), max_change)


	def policy(self, state):
		possible_actions = self.env.available_actions(state)
		numbers_left, dice_summation = state
		# Initialize with give up directly
		max_utility = self.giveup_reward(numbers_left)
		best_action = []
		
		for action in possible_actions:
			# Finish this part - Find the best action with utility computed in value iteration
			utility, state_s_prime_list = 0, self.env.all_transition_next(state[0], action)
			for state_s_prime in state_s_prime_list:
				utility += (state_s_prime[1] * self.utilities[state_s_prime[0]])
				if utility > max_utility:
					max_utility = utility
					best_action = action
			
		return best_action


if __name__=='__main__':
	env = Environment()
	# Try the following commands before coding
	# print(env.available_actions(State([1,2,3,4,5,6,7,8,9], 12)))
	# print(env.all_transition_next([1,2,3,4,5,6,7,8,9], [1,2]))


	agent = Agent(env)
	# Q1: Complete the Value iteration code here!
	agent.value_iteration()
	print('Utility of [1,2,3,4,5,6,7,8,9], 12: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9], 12)])
	print('Utility of [1,3,4,5,6,7,8,9], 12: %.3f' % agent.utilities[State([1,3,4,5,6,7,8,9], 12)])
	print('Utility of [1,3,5,6,7,8,9], 12: %.3f' % agent.utilities[State([1,3,5,6,7,8,9], 12)])
	# print('Utility of [], 8: %.3f' % agent.utilities[State([], 8)])
	# print('Utility of [1, 2, 7], 9: %.3f' % agent.utilities[State([1, 2, 7], 9)])
	# print('Utility of [2, 6, 8, 9], 5: %.3f' % agent.utilities[State([2, 6, 8, 9], 5)])
	# print('Utility of [1, 3, 4, 6, 9], 11: %.3f' % agent.utilities[State([1, 3, 4, 6, 9], 11)])
	# print('Utility of [1, 2, 3, 4, 5, 6, 7, 8, 9], 3: %.3f' % agent.utilities[State([1, 2, 3, 4, 5, 6, 7, 8, 9], 3)])
	
	# Q2: Complete policy function and run the code here!
	print('Optimal action of [1,2,3,4,5,6,7,8,9], 12: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9], 12))))
	print('Optimal action of [1,3,4,5,6,7,8,9], 12: %s' % str(agent.policy(State([1,3,4,5,6,7,8,9], 12))))
	print('Optimal action of [1,3,5,6,7,8,9], 12: %s' % str(agent.policy(State([1,3,5,6,7,8,9], 12))))
	# print('Optimal action of [], 8: %s' % str(agent.policy(State([], 8))))
	# print('Optimal action of [1, 2, 7], 9: %s' % str(agent.policy(State([1, 2, 7], 9))))
	# print('Optimal action of [2, 6, 8, 9], 5: %s' % str(agent.policy(State([2, 6, 8, 9], 5))))
	# print('Optimal action of [1, 3, 4, 6, 9], 11: %s' % str(agent.policy(State([1, 3, 4, 6, 9], 11))))
	# print('Optimal action of [1, 2, 3, 4, 5, 6, 7, 8, 9], 3: %s' % str(agent.policy(State([1, 2, 3, 4, 5, 6, 7, 8, 9], 3))))

	## Extra credit 1 - must change line 41 to self.total_numbers = 10
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 2: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 2)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 3: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 3)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 4: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 4)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 5: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 5)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 6: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 6)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 7: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 7)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 8: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 8)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 9: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 9)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 10: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 10)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 11: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 11)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10], 12: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10], 12)])
	
	
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 2: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 2))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 3: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 3))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 4: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 4))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 5: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 5))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 6: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 6))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 7: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 7))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 8: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 8))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 9: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 9))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 10: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 10))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 11: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 11))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10], 12: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10], 12))))
	
	## Extra credit 2 - must change line 41 to self.total_numbers = 12
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 2: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 2)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 3: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 3)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 4: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 4)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 5: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 5)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 6: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 6)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 7: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 7)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 8: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 8)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 9: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 9)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 10: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 10)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 11: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 11)])
	# print('Utility of [1,2,3,4,5,6,7,8,9,10,11,12], 12: %.3f' % agent.utilities[State([1,2,3,4,5,6,7,8,9,10,11,12], 12)])

	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 2: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 2))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 3: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 3))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 4: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 4))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 5: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 5))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 6: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 6))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 7: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 7))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 8: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 8))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 9: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 9))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 10: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 10))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 11: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 11))))
	# print('Optimal action of [1,2,3,4,5,6,7,8,9,10,11,12], 12: %s' % str(agent.policy(State([1,2,3,4,5,6,7,8,9,10,11,12], 12))))