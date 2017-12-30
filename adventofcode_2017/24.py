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

def bestFrom( port, used, part ):
    max_length = 0
    max_strength = 0

    # only consider components that aren't already used
    for next_component in ports[port].difference(used):
        next_port = components[next_component][0] if components[next_component][1] == port else components[next_component][1]
        next_used = used.copy()
        next_used.add( next_component)

        length, strength = bestFrom( next_port, next_used, part )

        length += 1
        strength += sum(components[next_component])

        # All we care about is strength.  Length for info
        if part == 1:
            if strength > max_strength:
                max_strength = strength
                max_length = length

        # All we care about is length.  Strength is only used for tie breakers
        if part == 2:
            if length > max_length:
                max_length = length
                max_strength = strength
            if length == max_length:
                if strength > max_strength:
                    max_strength = strength

    return max_length,max_strength

def main():
    input,part = getArgs()

    for i,line in enumerate(input):
        a,b = map(int,line.split('/'))
        components[i] = (a,b)
        ports[a].add(i)
        ports[b].add(i)

    print "The strongest bridge is %d long with strength %d" % bestFrom(0, set(), 1 )
    print "The longest bridge is %d long with strength %d" % bestFrom(0, set(), 2 )


if __name__=='__main__':
    main()
