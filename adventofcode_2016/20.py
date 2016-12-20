#!/usr/bin/env python

import sys
import os.path
from heapq import heapify,heappop,heappush

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

heap=[]
heapify( heap )

for line in content:
	if not line :
		continue
	parse=line.split('-')
	heappush(heap, ( int(parse[0]),int(parse[1]) ) )

next=0
maximum=9
count=0
printed=False

while heap:
	a,b=heappop(heap)
#	print "a: %d, b: %d" % (a,b)
	if next < a:
		count += a-next
		if not printed:
			print "The smallest allowed address is %d" % next
			printed=True
#		print "count: %d, next: %d" % (count,next)
	next=max(next,b+1)

if next <= maximum:
	count+=maximum-next+1

print "There are %d total allowed addresses" % count
sys.exit(0)
