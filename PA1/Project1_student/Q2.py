# Do not change the code framework - you could lose your grade
# Project 1 - Q2
import os
import heapq 
import collections
import numpy as np
# You can use the heapq library in python standard libraries to implement priority queues.
# Check the Python doc of heapq.heappop and heapq.heappush at https://docs.python.org/3/library/heapq.html

class SokubanSolver2:
	def __loadInput(self, filename):
		f = open(filename, 'r')
		rawinput = []
		for line in f.readlines():
			rawinput.append(line.strip())
		return rawinput

	def preprocess(self, input):
		output = []
		for i in range(len(input)):
			if "B" in input[i]:
				coordinate_B = [i,input[i].find("B")]
			if "P" in input[i]:
				coordinate_P = [i,input[i].find("P")]
			if "*" in input[i]:
				coordinate_star = [i,input[i].find("*")]
			output.append(list(input[i]))

		output[coordinate_B[0]][coordinate_B[1]], output[coordinate_P[0]][coordinate_P[1]], output[coordinate_star[0]][coordinate_star[1]] = ".", ".", "."
		return output, coordinate_B, coordinate_P, coordinate_star

	def heuristic(self, state, target):
		dist = np.linalg.norm(np.array(state)-np.array(target))
		return dist

	def move_keeper(self, map_array, B, P, star, distance):
		dir, push, cost, num = ([-1,0],[0,1],[1,0],[0,-1]), 0, 0, 0
		f_n = distance + cost
		start = {
			'player': np.array(P),
			'box': np.array(B),
			'push': push,
			'cost': cost,
			'f_n':  distance + cost
		}
		queue = collections.deque()
		queue.append(start)
		heap_queue = [((f_n, num, queue[0]))]
		num += 1
		heapq.heapify(heap_queue)
		
		visited = set()
		visited.add(((tuple(P),tuple(B))))

		while heap_queue:
			## Move to the next state which has the minimum f(n) value
			current_node = heapq.heappop(heap_queue)

			for i in range(len(dir)):
				new_x, new_y = current_node[2]['player'][0]+dir[i][0], current_node[2]['player'][1]+dir[i][1]
				
				if 0<=new_x<len(map_array) and 0<=new_y<len(map_array[0]) :
					if ((tuple([new_x,new_y]),tuple(current_node[2]['box'].tolist()))) not in visited:
						## if the keeper moves towards coordinate that has box
						if ([new_x,new_y] == current_node[2]['box'].tolist()):
							if 0<=new_x+dir[i][0]<len(map_array) and 0<=new_y+dir[i][1]<len(map_array[0]):
								if map_array[new_x+dir[i][0]][new_y+dir[i][1]]!="#":
									new_node = {
										'player': np.array([new_x, new_y]),
										'box': np.array([current_node[2]['box'][0]+dir[i][0],current_node[2]['box'][1]+dir[i][1]]),
										'push': current_node[2]['push']+1,
										'cost': current_node[2]['cost'],
										'f_n':  Solver.heuristic([new_x, new_y], star) + current_node[2]['cost']
									}
									heapq.heappush(heap_queue, (Solver.heuristic([new_x, new_y], star) + current_node[2]['cost'], num, new_node))
									num += 1
									visited.add((tuple([new_x,new_y]), tuple([current_node[2]['box'][0]+dir[i][0], current_node[2]['box'][1]+dir[i][1]])))

									## search problem reaches the goal state
									if [current_node[2]['box'][0]+dir[i][0],current_node[2]['box'][1]+dir[i][1]] == star:
										return current_node[2]['push']+1
						
						## if the keeper moves towards coordinate that doesn't have box
						else:
							if map_array[new_x][new_y]=="." :
								new_node = {
									'player': np.array([new_x, new_y]),
									'box': np.array(current_node[2]['box'].tolist()),
									'push': current_node[2]['push'],
									'cost': current_node[2]['cost']+1,
									'f_n':  Solver.heuristic([new_x, new_y], star) + current_node[2]['cost']
								}
								heapq.heappush(heap_queue, (Solver.heuristic([new_x, new_y], star) + current_node[2]['cost'], num, new_node))
								num += 1
								visited.add((tuple([new_x,new_y]), tuple([current_node[2]['box'][0], current_node[2]['box'][1]])))
		return -1

	def solve(self, inputFilename): 
		rawinput = self.__loadInput(inputFilename)
		# Implement this
		# Start with processing the input, get the initial state and game map - You can reuse what you did in Q1
		map_array, B, P, star = Solver.preprocess(rawinput)
		
		# Then implement the heuristic function above
		distance = Solver.heuristic(B, P)

		# Finally, implement the A* algorithm
		solution = Solver.move_keeper(map_array, B, P, star, distance)

		return solution


if __name__=='__main__':
	test_file_number = 5 # Change this to use different test files
	filename = 'game%d.txt' % test_file_number
	testfilepath = os.path.join('test','Q2', filename)
	Solver = SokubanSolver2()
	res = Solver.solve(testfilepath)

	ansfilename = 'ans%d.txt' % test_file_number 
	answerfilepath = os.path.join('test', 'Q2', ansfilename)
	f = open(answerfilepath, 'r')
	ans = int(f.readlines()[0].strip())

	print('Your answer is %d. True answer is %d.' % (res, ans))

	if res == ans:
		print('Answer is correct.')
	else:
		print('Answer is wrong.')