#!/usr/bin/env python

import sys
import os
import time
import numpy as np

cols=50
rows=6

def print_panel():
	tmp=os.system('clear')
	for i in range(rows):
		for j in range(cols):
			if panel[i][j]:
				print '#',
			else:
				print ' ',
		print
	time.sleep(0.02)

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

panel=np.zeros((rows,cols), dtype=bool)

print_panel()

for line in content:
	buffer=line.split()
	if buffer[0]=='rect':
		coords=buffer[1].split('x')
		for i in range(int(coords[1])):
			for j in range(int(coords[0])):
				panel[i][j]=1
	if buffer[0]=='rotate':
		ind=int(buffer[2].split('=')[-1])
		mag=int(buffer[4])
		if buffer[1]=='row':
			panel[ind]=np.roll(panel[ind],mag)
		else: #column
			panel[:,ind]=np.roll(panel[:,ind],mag)
	print_panel()

print "That took",np.sum(panel),"pixels"

sys.exit(0)
