#!/usr/bin/env python

import sys
import os.path
from math import sqrt

def readInput():
	if len(sys.argv) == 2:
		return int(sys.argv[1])
	else:
		usageAndExit()

def usageAndExit():
	print "19.py"
	sys.exit(1)

def factors(n):
	step = 2 if n%2 else 1
	return set( reduce( list.__add__, ([i, n//i] for i in range(1, int(sqrt(n))+1, step) if n % i == 0) ) )

def main():
	limit = readInput()
	part_limit = limit / 10
	can = part_limit / 5 ## a little number-theory sleuthings shows that suberabudant numbers tend have factors sums of 4-5x themselves in this range
	can_sum = 0

	while can_sum < part_limit:
		can += 1
		can_sum = sum( factors(can) )

	print "House %d is the winner of part 1 with %d presents!" % (can,can_sum*10)

	can_sum = 0
	part_limit = limit / 11

	while can_sum < part_limit:
		can += 1
		can_sum = 0
		for i in range(1,50):
			if not can % i:
				can_sum += can / i

	print "House %d is the winner of part 2 with %d presents!" % (can,can_sum*11)

if __name__ == '__main__':
	main()

sys.exit(0)
