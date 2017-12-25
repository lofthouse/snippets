#!/usr/bin/env python
import sys
import os
from collections import defaultdict

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 3 :
        print "Invalid argument"
        print "%s <input file> <part>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    part = int(sys.argv[2])

    if not (part == 1 or part == 2):
        print "%s is not a valid part" % sys.argv[2]
        sys.exit(1)

    return (input,part)

# Begin actual code

def read(arg, registers):
    debug( "Reading", arg )

    if isinstance( arg, list ):
        arg = arg[0]

    if isinstance( arg, str ) and arg.isalpha():
        return registers[arg]
    else:
        return int(arg)

def main():
    input,part = getArgs()
    registers = defaultdict(int)
    instruction = 0

    while True:
        line = input[instruction].split()
        debug( line )

        (cmd,reg),arg = line[0:2],line[2:]

        if cmd == 'snd':
            registers['freq'] = read(reg,registers)

        if cmd == 'set':
            registers[reg] = read(arg,registers)

        if cmd == 'add':
            registers[reg] = registers[reg] + read(arg,registers)

        if cmd == 'mul':
            registers[reg] = registers[reg] * read(arg,registers)

        if cmd == 'mod':
            registers[reg] = registers[reg] % read(arg,registers)

        if cmd == 'rcv':
            if read(reg,registers) != 0:
                print "RECOVERED %d" % registers['freq']
                sys.exit(0)

        if cmd == 'jgz' and read(reg,registers) != 0:
                instruction = instruction + read(arg,registers)
        else:
            instruction = instruction + 1

        debug( registers )


if __name__=='__main__':
    main()
