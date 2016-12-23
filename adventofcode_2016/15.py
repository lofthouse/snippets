#!/usr/bin/env python

import sys
import os.path

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

print "%d instructions loaded" % len(content)

disks=[]

def addDisk(line):
	global disks

	parse=line.split()

	#pre-rotate by position in stack so state always shows disk as seen by capsule falling at time
	offset=int(parse[1][1:])
	positions=int(parse[3])
	position=int(parse[11][:-1])

	disks.append( ((position+offset) % positions,positions) )

for line in content:
	addDisk(line)

time=0
while not all( disk[0]==0 for disk in disks ):
#	print disks
	disks=[ ( (disk[0]+1) % disk[1], disk[1]) for disk in disks ]
#	print disks
	time += 1
#	_=raw_input("Enter to continue...")


print "Dropping at time %d would be a sneaky idea!" % time

