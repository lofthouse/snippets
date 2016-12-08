#!/usr/bin/env python

import sys
import hashlib
import json
import os.path

def hashDict(dictionary):
	return hashlib.md5(json.dumps(dictionary, sort_keys=True)).hexdigest()

def getinput(wires,gate):
	return int(gate) if gate.isdigit() else wires[gate]

# tick each operator until we reach steady state (hash doesn't change)
def findSteadyState(wires,gates,wire):
	hash=''
	while hash != hashDict(wires) :
		hash = hashDict(wires)
		for gate in gates:
			gate.tick(wires)
	print "Wire",wire,"is",wires[wire]

class monoGate:
	def __init__(self,in_A,out,wires):
		self.in_A=in_A
		self.out=out
		wires[self.out]=0

class biGate:
	def __init__(self,in_A,in_B,out,wires):
		self.in_A=in_A
		self.in_B=in_B
		self.out=out
		wires[self.out]=0

class ANDGate(biGate):
	def tick(self,wires):
		wires[self.out] = getinput(wires,self.in_A) & getinput(wires,self.in_B)

class ORGate(biGate):
	def tick(self,wires):
		wires[self.out] = getinput(wires,self.in_A) | getinput(wires,self.in_B)

class LSHIFTGate(biGate):
	def tick(self,wires):
		wires[self.out] = getinput(wires,self.in_A) << getinput(wires,self.in_B)

class RSHIFTGate(biGate):
	def tick(self,wires):
		wires[self.out] = getinput(wires,self.in_A) >> getinput(wires,self.in_B)

class NOTGate(monoGate):
	def tick(self,wires):
		wires[self.out] = 0xffff & ~ getinput(wires,self.in_A)

class ASSIGNGate(monoGate):
	def tick(self,wires):
		wires[self.out]=getinput(wires,self.in_A)


with open(sys.argv[1]) as input_file:
	content = input_file.read().splitlines()

gates=[]
wires={}

for line in content:
	if not line :
		continue
	parse=line.split()
	if 'AND' in parse:
		gates.append(    ANDGate(parse[0],parse[2],parse[4],wires) )
	elif 'OR' in parse:
		gates.append(     ORGate(parse[0],parse[2],parse[4],wires) )
	elif 'LSHIFT' in parse:
		gates.append( LSHIFTGate(parse[0],parse[2],parse[4],wires) )
	elif 'RSHIFT' in parse:
		gates.append( RSHIFTGate(parse[0],parse[2],parse[4],wires) )
	elif 'NOT' in parse:
		gates.append(    NOTGate(parse[1],parse[3],wires) )
	else:
		gates.append( ASSIGNGate(parse[0],parse[2],wires) )

findSteadyState(wires,gates,'a')

# remove the gate that assigns a fixed value to b
gates = [ gate for gate in gates if not gate.out == 'b' ]
# and add a new one with a's value
gates.append(ASSIGNGate(str(wires['a']),'b',wires))

findSteadyState(wires,gates,'a')

sys.exit(0)
