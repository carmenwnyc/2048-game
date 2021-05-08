import random
from BaseAI import BaseAI
from Grid import Grid
import time
import math

MAX_DEPTH = 3
TIME_LIMIT = 0.195

directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
directionMap = {
    0: UP_VEC,
    1: RIGHT_VEC,
    2: DOWN_VEC,
    3: LEFT_VEC,
}

WEIGHT_MONOTONICITY = pow(4,4)
WEIGHT_SMOOTHNESS = 2000
WEIGHT_MERGE_CELLS = 3792
WEIGHT_EMPTY_CELLS = 1224

class IntelligentAgent(BaseAI):
    def getMove(self, grid):
    	alpha = float('-inf')
    	beta = float('inf')
    	start_time = time.process_time()
    	move, value = self.maximize(grid, alpha, beta, start_time,0)
    	return move

    def maximize(self, grid, alpha, beta, start_time, current_depth):
    	current_depth += 1
    	if self.terminal_test(grid, start_time, current_depth):
    		return None, self.utility(grid)

    	bestMove = None
    	value = float('-inf')

    	for item in grid.getAvailableMoves():
    		move = item[0]
    		movedGrid = item[1]
    		temp = self.minimize(movedGrid, alpha, beta, start_time, current_depth, 2) * 0.9 + self.minimize(movedGrid, alpha, beta, start_time, current_depth, 4) * 0.1

    		if temp > value:
    			value = temp
    			bestMove = move

    		if value >= beta:
    			return move, value

    		alpha = max(alpha, value)	
    	return bestMove, value

    def minimize(self, grid, alpha, beta, start_time, current_depth, tileValue):
    	current_depth += 1
    	if self.terminal_test(grid, start_time, current_depth):
    		return self.utility(grid)

    	value = float('inf')

    	for cell in grid.getAvailableCells():
    		newGrid = grid.clone()
    		newGrid.setCellValue(cell, tileValue)
    		value = min(value, self.maximize(newGrid, alpha, beta, start_time, current_depth)[1])

    		if value <= alpha:
    			return value
    		beta = min(beta, value)
    	
    	return value

    def terminal_test(self, grid, start_time, current_depth):
    	now = time.process_time()
    	if now - start_time > TIME_LIMIT or not grid.canMove() or current_depth > MAX_DEPTH:
    		return True

    def utility(self, grid):
    	smoothness = self.smoothness(grid)
    	monotonicity = self.snake(grid)
    	merge, empty= self.merge_empty(grid)
    	return WEIGHT_MONOTONICITY * monotonicity + WEIGHT_SMOOTHNESS * smoothness + WEIGHT_MERGE_CELLS * merge + WEIGHT_EMPTY_CELLS * empty

    def snake(self, grid):
    	"""monotonicity heuristics""" 
    	"""source: http://cs229.stanford.edu/proj2016/report/NieHouAn-AIPlays2048-report.pdf """
    	size = grid.size
    	weight_matrix = [[0] * size for i in range(size)]
    	for i in range(size):
    		power = abs(i - size) * size - 1
    		if i % 2 == 0:
    			for j in range(size):
    				weight_matrix[i][j] = power
    				power -= 1
    		else:
    			for j in reversed(range(size)):
    				weight_matrix[i][j] = power
    				power -= 1
    	# print(weight_matrix)
    	sum = 0
    	for i in range(size):
    		for j in range(size):
    			sum += (weight_matrix[i][j] * grid.map[i][j])
    	return sum

    def findFarthestPos(self, pos, grid, direction_vec): # -> tuple(row, col)
    	"""given an occupied cell location "pos", find the farthest spot it could move to """
    	# Progress towards the vector direction until an obstacle is found
    	# pos is a tuple of (x,y) indicating position of a cell on the grid
    	# direction_vec one of the vectors in directionVectors tuples
    	prev = pos
    	currPos = (prev[0] + direction_vec[0], prev[1] + direction_vec[1])
    	while grid.crossBound(currPos) and grid.map[currPos[0]][currPos[1]] == 0:
    		prev =currPos
    		currPos = (prev[0] + direction_vec[0], prev[1] + direction_vec[1])

    	farthest = prev
    	return farthest

    def next(self, pos, grid, direction_vec): # -> tuple(row, col)
    	""" find the next legal cell position on the grid, based on the direction and current position"""
    	# direction_vec one of the vectors in directionVectors tuples
    	next = (pos[0] + direction_vec[0], pos[1] + direction_vec[1])
    	if grid.crossBound(next):
    		return next
    	else:
    		return pos

    def smoothness(self, grid):
    	"""Smoothness heuristic measures the difference between neighboring tiles and tries to minimize this count"""
    	### source: https://github.com/ronzil/2048-AI/blob/master/js/grid.js
    	smoothness = 0
    	for i in range(grid.size):
    		for j in range(grid.size):
    			if grid.map[i][j] != 0:
    				value = math.log(grid.map[i][j])/math.log(2)
    				for direction in range(1,3): # only need to do down and right, two directions; up and left are the same
    					dir_vec = directionMap[direction]
    					farthestCell = self.findFarthestPos((i, j), grid, dir_vec)
    					targetCell = self.next(farthestCell, grid, dir_vec)
    					if grid.map[targetCell[0]][targetCell[1]] != 0:
    						targetValue = math.log(grid.map[targetCell[0]][targetCell[1]])/math.log(2)
    						smoothness -= abs(value - targetValue)
    	return smoothness
    									

    def merge_empty(self, grid):
    	""" Heuristic to get the number of mergable cells and empty cells in the whole board"""
    	merge_horizontal = 0
    	merge_vertical = 0
    	mergedOnce = False
    	empty = 0
    	for i in range(grid.size):
    		prev = None
    		for j in range(grid.size):
    			current = grid.map[i][j]
    			if current!=0:
	    			if prev == current and not mergedOnce:
	    				merge_horizontal += 1
	    				mergedOnce = True
	    			if prev != current and mergedOnce:
	    				mergedOnce = False
	    			prev = current
	    		else:
	    			empty += 1

    	mergedOnce = False
    	for j in range(grid.size):
    		prev = None
    		for i in range(grid.size):
    			current = grid.map[i][j]
    			if current!=0:
	    			if prev == current and not mergedOnce:
	    				merge_vertical += 1
	    				mergedOnce = True
	    			if prev != current and mergedOnce:
	    				mergedOnce = False
	    			prev = current

    	return max(merge_horizontal, merge_vertical), empty




