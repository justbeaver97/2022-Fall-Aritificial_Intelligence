# Do not change the code framework - you could lose your grade
# Project 1 - Q1
import os
import collections

class SokubanSolver1:
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

	def total_moves(self, map_array, B, P, star, cost):
		dir = ([-1,0],[0,1],[1,0],[0,-1])
		start = (P, B, cost)
		visited = set()
		visited.add(((tuple(P),tuple(B))))

		queue = collections.deque([start])
		while queue:
			## move to the next state in the queue
			current_node = queue.popleft()

			for i in range(len(dir)):
				new_x = current_node[0][0]+dir[i][0]
				new_y = current_node[0][1]+dir[i][1]

				if 0<=new_x<len(map_array) and 0<=new_y<len(map_array[0]) and ((tuple([new_x,new_y]),tuple([current_node[1][0],current_node[1][1]]))) not in visited:
					## if the keeper moves towards coordinate that has box
					if [new_x,new_y] == current_node[1]:
						if 0<=new_x+dir[i][0]<len(map_array) and 0<=new_y+dir[i][1]<len(map_array[0]):
							if map_array[new_x+dir[i][0]][new_y+dir[i][1]]!="#":
								new_node = ([new_x, new_y], [current_node[1][0]+dir[i][0],current_node[1][1]+dir[i][1]], current_node[2]+1)
								visited.add((tuple([new_x,new_y]),tuple([current_node[1][0]+dir[i][0],current_node[1][1]+dir[i][1]])))
								queue.append(new_node)

								## search problem reaches the goal state
								if [current_node[1][0]+dir[i][0],current_node[1][1]+dir[i][1]] == star:
									return current_node[2]+1
					
					## if the keeper moves towards coordinate that doesn't have box
					else:
						if map_array[new_x][new_y]=="." :
							new_node = ([new_x, new_y], current_node[1], current_node[2]+1)
							visited.add((tuple([new_x,new_y]),tuple([current_node[1][0],current_node[1][1]])))
							queue.append(new_node)
		return -1

	def solve(self, inputFilename): 
		rawinput = self.__loadInput(inputFilename)
		# Implement this
		# Start with processing the input, get the initial state and game map 
		map_array, B, P, star = Solver.preprocess(rawinput)

		# Then implement a search function
		solution = Solver.total_moves(map_array, B, P, star, cost = 0)
		
		return solution


if __name__=='__main__':
	test_file_number = 5 # Change this to use different test files
	filename = 'game%d.txt' % test_file_number
	testfilepath = os.path.join('test','Q1', filename)
	Solver = SokubanSolver1()
	res = Solver.solve(testfilepath)

	ansfilename = 'ans%d.txt' % test_file_number 
	answerfilepath = os.path.join('test', 'Q1', ansfilename)
	f = open(answerfilepath, 'r')
	ans = int(f.readlines()[0].strip())

	print('Your answer is %d. True answer is %d.' % (res, ans))

	if res == ans:
		print('Answer is correct.')
	else:
		print('Answer is wrong.')