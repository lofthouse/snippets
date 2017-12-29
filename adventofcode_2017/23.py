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
        self.instruction = 0
        self.blocked = False
        self.mulcount = 0

    def tick(self):
        line = self.instructions[self.instruction].split()
        debug( self.instruction, ":", line )

        (cmd,reg),arg = line[0:2],line[2:]

        if cmd == 'set':
            self.registers[reg] = self.read(arg)

        if cmd == 'sub':
            self.registers[reg] -= self.read(arg)

        if cmd == 'mul':
            self.registers[reg] *= self.read(arg)
            self.mulcount += 1

        if cmd == 'jnz' and self.read(reg) != 0:
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

    prog = program(0,input)

    while not (prog.blocked) and not (prog.jmpfault):
        prog.tick()
        debug( prog.registers )
    else:
        print "Jump Fault!"

        print "Mulcount:",prog.mulcount
        print "Registers:",prog.registers
        print "Instruction:",prog.instruction
        sys.exit(0)

if __name__=='__main__':
    main()
