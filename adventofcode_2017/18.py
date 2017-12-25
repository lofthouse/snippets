#!/usr/bin/env python
import sys
import os
from collections import defaultdict
from collections import deque

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 2 :
        print "Invalid argument"
        print "%s <input file>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    return input

# Begin actual code
class program():
    def __init__(self,ID,instructions):
        self.ID = ID
        self.instructions = instructions
        self.jmpfault = False
        self.registers = defaultdict(int)
        self.registers['p'] = ID
        self.instruction = 0
        self.blocked = False
        self.buffer = deque()
        self.sendcount = 0

    def deliver(self, value):
        self.buffer.append(value)

    def tick(self,progs):
        line = self.instructions[self.instruction].split()
        debug( self.ID, ":", line )

        (cmd,reg),arg = line[0:2],line[2:]

        if cmd == 'snd':
            progs[ 1-self.ID ].deliver( self.read(reg) )
            self.sendcount = self.sendcount + 1

        if cmd == 'set':
            self.registers[reg] = self.read(arg)

        if cmd == 'add':
            self.registers[reg] = self.registers[reg] + self.read(arg)

        if cmd == 'mul':
            self.registers[reg] = self.registers[reg] * self.read(arg)

        if cmd == 'mod':
            self.registers[reg] = self.registers[reg] % self.read(arg)

        if cmd == 'rcv':
            if len( self.buffer ) != 0:
                if self.blocked:
                    self.blocked = False
                self.registers[reg] = self.buffer.popleft()
            elif not self.blocked:
                self.blocked = True

        if cmd == 'jgz' and self.read(reg) > 0:
                self.instruction = self.instruction + self.read(arg)
        elif not self.blocked:
            self.instruction = self.instruction + 1

        if self.instruction < 0 or self.instruction >= len(self.instructions):
            self.jmpfault = True

    def read(self, arg):
        if isinstance( arg, list ):
            arg = arg[0]

        if isinstance( arg, str ) and arg.isalpha():
            return self.registers[arg]
        else:
            return int(arg)

def main():
    input = getArgs()

    progs = [ program(0,input), program(1,input) ]

    while not (progs[0].blocked and progs[1].blocked) and not (progs[0].jmpfault or progs[1].jmpfault):
        for i in range(2):
            progs[i].tick(progs)
            debug( progs[i].registers )
    else:
        if progs[0].blocked and progs[1].blocked:
            print "Deadlocked!"
        else:
            print "Jump Fault!"

        for i in range(2):
            print "Program %d:" %i
            print "Sendcount:",progs[i].sendcount
            print "Registers:",progs[i].registers
            print "Instruction:",progs[i].instruction
        sys.exit(0)

if __name__=='__main__':
    main()
