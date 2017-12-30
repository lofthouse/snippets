#!/usr/bin/env python
import sys
import os
from collections import defaultdict

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 2 :
        print "Invalid argument"
        print "%s <input file> <part>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    return input

# Begin actual code

class SM():
    def __init__(self,state,state_rules):
        self.state_rules = state_rules
        self.state = state
        self.tape = defaultdict(int)
        self.slot = 0

    def tick(self):
        write,inc,next = self.state_rules[ (self.state,self.tape[self.slot]) ]

        self.tape[self.slot] = write
        self.slot += inc
        self.state = next

    def diagnostic(self):
        print "Checksum:",sum( self.tape.values() )

def parseInput( input ):
    state = input[0].split()[3].strip('.')
    steps = int( input[1].split()[5] )
    state_rules = {}

    in_state = False
    in_value = False

    for line in input[3:]:
        line = line.strip('.').strip(':')
        pieces = line.split()

        if len( pieces ) == 0:
            in_state = False
            in_value = False
        elif not in_state:
            sr_state = line.split()[2]
            in_state = True
        elif not in_value:
            sr_value = int( line.split()[5] )
            in_value = True
        else:
            if pieces[1] == 'Write':
                sr_write = int( pieces[4] )
            elif pieces[1] == 'Move':
                sr_inc = 1 if pieces[6] == 'right' else -1
            elif pieces[1] == 'Continue':
                sr_next = pieces[4]

                # End of the data gathering for a rule
                state_rules[ (sr_state,sr_value) ] = (sr_write, sr_inc, sr_next)
                in_value = False

    return steps, SM( state, state_rules )


def main():
    input = getArgs()

    steps, state_machine = parseInput( input )

    for i in range( steps ):
        if i%1000 == 0:
            print "\rStep",i,
        state_machine.tick()

    print
    state_machine.diagnostic()


if __name__=='__main__':
    main()
