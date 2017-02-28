#!/usr/bin/env python

import sys
import os.path

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

	grid=[]
	for j in range(dim):
		grid.append( [ 1 if i=='#' else 0 for i in list(content[j]) ] )

	return dim, iters, grid

def step(dim, grid, part2 = False):
	result = [ [ 0 for i in range(dim) ] for i in range(dim) ]

	for j in range(dim):
		for i in range(dim):
			neighbors = [ grid[y][x] for x in range(max(0,i-1),min(dim,i+2)) for y in range(max(0,j-1),min(dim,j+2)) ]

			if grid[j][i] == 1:
				if sum(neighbors) - 1 in (2,3):
					result[j][i] = 1
			else:
				if sum(neighbors) == 3:
					result[j][i] = 1
	if part2:
		for j in 0,dim-1:
			for i in 0,dim-1:
				result[j][i] = 1

	return result

def main():
	for mode in False,True:
		dim, iters, grid = readGrid()
		for _ in range(iters):
			grid = step(dim,grid,mode)

		count = 0
		for row in grid:
			count = count + sum(row)
#			print ''.join(map(str,row))

		print "There are %d lights on for %s" % (count, 'part 2' if mode==True else 'part 1')

if __name__ == '__main__':
	main()

sys.exit(0)
