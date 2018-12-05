#! /usr/bin/env python3
import os
import sys
from collections import defaultdict
import re
import operator

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()


def main():
    lines = readfile()
    events = []

    for line in lines:
        events.append( re.findall('\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.+)', line)[0] )
    events = sorted(events)

    guard_stats = defaultdict( lambda: [ 0 for i in range(60)] )
    for event in events:
        details = event[5].split()
        if details[0] == 'Guard':
            ID = details[1]
        elif details[0] == 'falls':
            start = int( event[4] )
        elif details[0] == 'wakes':
            end = int( event[4] )
            for minute in range(start,end):
                guard_stats[ID][minute] += 1

    laziness = [ ( sum(guard_stats[i]),i) for i in guard_stats ]
    _,lazy = max(laziness)

    cs = int( lazy[1:] ) * guard_stats[lazy].index( max( guard_stats[lazy] ) )
    print( f"The laziest guard is {lazy} with a checksum of {cs}")

    minutes = { g: max( guard_stats[g] ) for g in guard_stats}
    minuteman = max(minutes.items(), key=operator.itemgetter(1))[0]

    cs = int( minuteman[1:] ) * guard_stats[minuteman].index( max( guard_stats[minuteman] ) )
    print( f"The laziest guard is {minuteman} with a checksum of {cs}")

if __name__ == "__main__":
    main()
