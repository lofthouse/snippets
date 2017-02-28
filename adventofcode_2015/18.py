#!/usr/bin/env python

import sys
import os.path
import collections

def usageAndExit():
	print "18.py <grid_dim> <iterations> <input_file>"
	sys.exit(1)

def readGrid():
	if len(sys.argv) == 4 and sys.argv[1].isdigit() and sys.argv[2].isdigit() and os.path.isfile(sys.argv[3]):
		dim = int(sys.argv[1])
		iters = int(sys.argv[2])
	else:
		usageAndExit()

	with open(sys.argv[3]) as input_file:
		content = input_file.read().splitlines()

	grid = [ [ 0 for i in range(dim) ] for i in range(dim) ]

	j = 0
	for line in content:
		i = 0
		for char in line:
			grid[j][i] = 1 if char=='#' else 0
			i = i + 1
		j = j + 1

	return dim, iters, grid

def step(dim, grid):
	neighbor_counts = [ [ 0 for i in range(dim) ] for i in range(dim) ]
	result = [ [ 0 for i in range(dim) ] for i in range(dim) ]

	for j in range(dim):
		for i in range(dim):
			neighbors = [ grid[y][x] for x in range(max(0,i-1),min(dim,i+2)) for y in range(max(0,j-1),min(dim,j+2)) ]
			neighbor_counts[j][i] = sum(neighbors) - grid[j][i]

			if grid[j][i] == 1:
				if sum(neighbors) - 1 in (2,3):
					result[j][i] = 1
			else:
				if sum(neighbors) == 3:
					result[j][i] = 1

	for j in 0,dim-1:
		for i in 0,dim-1:
			result[j][i] = 1

	return result

def main():
	dim, iters, grid = readGrid()
	for _ in range(iters):
		grid = step(dim,grid)

	print "There are %d lights on" % reduce(lambda x, y: x + sum(y), grid, 0)

if __name__ == '__main__':
	main()

sys.exit(0)
