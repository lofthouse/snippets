#! /usr/bin/env python3
import os
import sys
from collections import defaultdict
import re
import operator
import pprint as pp

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

#    pp.pprint( events )

    guard_stats = defaultdict( lambda: defaultdict(int) )
    for event in events:
        # ('1518', '08', '28', '23', '56', 'Guard #1559 begins shift'),
        # ('1518', '08', '29', '00', '47', 'falls asleep'),
        # ('1518', '08', '29', '00', '59', 'wakes up'),
        details = event[5].split()
        if details[0] == 'Guard':
            ID = details[1]
        elif details[0] == 'falls':
            start = int( event[4] )
        elif details[0] == 'wakes':
            end = int( event[4] )
            for minute in range(start,end):
                guard_stats[ID][minute] += 1
        else:
            print( "ERROR!")
            print( event )

#    pp.pprint(guard_stats)
    laziness = [ (sum(guard_stats[i].values()),i) for i in guard_stats ]
#    pp.pprint( laziness )
#    laziness = sorted( laziness )
#    pp.pprint( laziness )
    _,lazy = max(laziness)

#    pp.pprint( guard_stats[lazy])

    cs = int( lazy[1:] ) * max(guard_stats[lazy].items(), key=operator.itemgetter(1))[0]
    print( f"The laziest guard is {lazy} with a checksum of {cs}")

    minutes = { g: max( guard_stats[g].values() ) for g in guard_stats}
    minuteman = max(minutes.items(), key=operator.itemgetter(1))[0]

    pp.pprint( guard_stats[minuteman])

    cs = int( minuteman[1:] ) * max(guard_stats[minuteman].items(), key=operator.itemgetter(1))[0]
    print( f"The laziest guard is {minuteman} with a checksum of {cs}")

if __name__ == "__main__":
    main()
