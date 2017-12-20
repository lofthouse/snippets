#!/usr/bin/env python
import sys
import os.path

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

def readInput( input ):
    # tuple is needed, otherwise just a generator is returned
    return tuple( int(x) for x in input[0].split() )

def redestribute ( memory ):
#    value,target = max((v,i) for i,v in enumerate(memory))
    # index always returns the first location of the value
    # the above is more pythonic, but doesn't reliably return the first location
    value = max(memory)
    target = memory.index(value)

    # the working copy needs to be mutable, so create a list from the tuple provided
    mem = list(memory)
    mem[target] = 0

    while value > 0:
        target = target + 1
        value = value - 1
        mem[ target % len(mem) ] = mem[ target % len(mem) ] + 1

    # return an immutable tuple from the final version of the liset
    return tuple(mem)

def main():
    input = getArgs()

    # banks must be a tuple, because only immutable keys are allowed in sets
    # tuples are immutable, but lists are not
    banks = readInput( input )
#    print banks
    # for Part 2, we need to know the order of the history, hence this is now a list
    # this takes WAY longer than a set!!!
    history = []
    cycles = 0

    while banks not in history:
        history.append(banks)
        cycles = cycles + 1
        banks = redestribute( banks )
#        print banks

    print "It took %d cycles to repeat" % cycles

    print "The loop is %d long (starting at %d)" % (cycles - history.index(banks), history.index(banks) )

if __name__=='__main__':
    main()
