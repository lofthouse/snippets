#!/usr/bin/env python

import sys
import string

if len(sys.argv) == 3 and all(map(str.isdigit,sys.argv[1:])):
	disk_length=int(sys.argv[1])
	seed=sys.argv[2]
else:
	print "Usage:  16.py <disk_length> <seed_value>"
	sys.exit(0)

def createData(length,seed):
	trans=string.maketrans('01','10')

	data=seed
	while len(data) < length:
		b=data[::-1]
		b=string.translate(b,trans)
		data=data + '0' + b

	return data[:length]

def createChecksum(data):
	if (len(data) % 2) == 1:
		return data

	cs=''
	for n in range(0,len(data),2):
		cs += '1' if  data[n] == data[n+1] else '0'
	if (len(cs) % 2) == 0:
		return createChecksum(cs)
	else:
		return cs


data=createData(disk_length,seed)
checksum=createChecksum(data)

print "Final Checksum:",checksum
