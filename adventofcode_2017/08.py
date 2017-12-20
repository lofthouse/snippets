#!/usr/bin/env python
import sys
import os.path
from collections import defaultdict

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

def execute( ins, regs, record ):
    reg,op,arg,_,cmpreg,cmp,ref = ins.split()

    if test( regs[cmpreg], cmp, int(ref) ):
        if op == 'inc':
            regs[reg] = regs[reg] + int(arg)
        else:
            regs[reg] = regs[reg] - int(arg)

    max_register = max(regs,key=regs.get)
    if regs[max_register] > record[1]:
        record[0] = max_register
        record[1] = regs[max_register]

def test( value, op, arg ):
    if op == '<':
        return value < arg
    if op == '<=':
        return value <= arg
    if op == '==':
        return value == arg
    if op == '!=':
        return value != arg
    if op == '>=':
        return value >= arg
    if op == '>':
        return value > arg

def main():
    input = getArgs()
    registers = defaultdict(int)

    record = ['foo',0]

    for line in input:
        execute(line, registers, record)

    print "Register %s was the record holder, with value %d" % tuple(record)

    max_register = max(registers,key=registers.get)
    print "Register %s is the largest, with value %d" % (max_register,registers[max_register])

if __name__=='__main__':
    main()
