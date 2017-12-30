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

components = {}
ports = defaultdict(set)

def strongestFrom( port, used ):
    max_strength = 0

#    print "Starting SF from",port,"having used",used

    # only consider components that aren't already used
    for next_component in ports[port].difference(used):
#        print "Trying component",next_component,components[next_component]
        next_port = components[next_component][0] if components[next_component][1] == port else components[next_component][1]
#        print "The next port will be",next_port
        next_used = used.copy()
        next_used.add( next_component)
#        print "The next used list is",next_used

        strength = sum(components[next_component]) + strongestFrom( next_port, next_used )

        if strength > max_strength:
            max_strength = strength

    return max_strength

def main():
    input,part = getArgs()

    for i,line in enumerate(input):
        a,b = map(int,line.split('/'))
        components[i] = (a,b)
        ports[a].add(i)
        ports[b].add(i)

    print "The strongest bridge is", strongestFrom( 0, set() )


if __name__=='__main__':
    main()
