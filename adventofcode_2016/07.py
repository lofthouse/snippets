#!/usr/bin/env python

import sys
import os.path
import collections

TLScount=0
SSLcount=0

def hasTLS(line):
	inbracket=False
	candidate=False

	for n in range(len(line)-3):
		if inbracket:
			if line[n] == ']':
				inbracket=False
				continue
		if line[n] == '[':
			inbracket=True
			continue

#		a=line[n]
#		b=line[n+1]
#		if a != b and line[n+2] == b and line[n+3] == a:
		if line[n] != line[n+1] and line[n:n+2] == line[n+3:n+1:-1] :
			if inbracket :
				return False
			else:
				candidate=True
	return candidate

def hasSSL(line):
	inbracket=False
	candidate=False

	for n in range(len(line)-2):
		if inbracket:
			if line[n] == ']':
				inbracket=False
			continue
		if line[n] == '[':
			inbracket=True
			continue

		a=line[n]
		b=line[n+1]
		if a != b and line[n+2] == a :
			if BABsearch(line,b,a) :
				return True

	return False

def BABsearch(line,b,a):
	inbracket=False
	candidate=False

	for n in range(len(line)-4):
		if inbracket:
			if line[n] == ']':
				inbracket=False
				continue
			if line[n:n+3] == b+a+b :
				return True
		else:
			if line[n] == '[':
				inbracket=True
				continue
	return False

if  len(sys.argv) != 2 or not os.path.isfile(sys.argv[1]) :
	print "Invalid argument"
	sys.exit(1)

with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

for line in content:
	if hasTLS(line) :
		TLScount += 1
	if hasSSL(line) :
		SSLcount +=1

print "There are",TLScount,"IPs supporting TLS"
print "There are",SSLcount,"IPs supporting SSL"

sys.exit(0)
