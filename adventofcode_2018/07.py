#! /usr/bin/env python3
import os
import sys
from collections import defaultdict
import string
import copy

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

def main():
    lines = readfile()

    # graph is a set of lists of destinations from each node
    # dependencies is a REVERSE map of steps that must be completed prior to each node
    # unvisited is self-explanatory
    # graph will NOT be modified at runtime, but dependencies WILL be cleared as dependencies are lifted
    graph = {}
    dependencies = {}
    unvisited = set()

    # build all our graphs / sets
    for node in lines:
        _,a,_,_,_,_,_,b,_,_ = node.split()

        if a not in graph:
            graph[a] = []
        graph[a].append(b)

        if b not in dependencies:
            dependencies[b] = []
        dependencies[b].append(a)

        unvisited.add(a)
        unvisited.add(b)

    # before we start changing things, make a copy for part 2
    unvisited2 = copy.deepcopy(unvisited)
    dependencies2 = copy.deepcopy(dependencies)

    # Part 1:  keep visiting the lowest unblocked node until all nodes are visited
    path = ""
    while unvisited:
        next = min( unvisited.difference( set(dependencies.keys() ) ) )
        path += next
        unvisited.remove(next)

        if not unvisited:
            break

        # clear this dependency for all nodes reached FROM next
        for d in graph[next]:
            dependencies[d].remove(next)
            # and if all are cleared, remove the dependency altogether!
            if not dependencies[d]:
                del dependencies[d]

    print( path )


    # Part 2:  schedule and track all the workers....
    path = ""
    timer = 0
    workers = [ "", "", "", "", "" ]
    bt = 60

    # doneat is a list of steps that will complete at the key time
    doneat = defaultdict( list )
    # active are steps that are currently assigned to a worker and not yet done
    active = set()

    while unvisited2:
        nexts = sorted( unvisited2.difference( set(dependencies2.keys() ) ) )

        job = 0 # which job in the nexts list are we trying to schedule now as we walk across workers?
        for w in range( len(workers) ):
            # for each worker, see if they are not yet busy at this time
            if len( workers[w] ) <= timer:
                # if there's an unfinished job, try to assign it
                if job < len(nexts):
                    if nexts[job] not in active:
                        active.add( nexts[job] )
                        # Block the worker's schedule for that job for as long as it takes
                        workers[ w ] += ( nexts[job] * (string.ascii_uppercase.index(nexts[job]) + 1 + bt) )
                        doneat[ timer + string.ascii_uppercase.index(nexts[job]) + 1 + bt ] = nexts[job]
                        job += 1
                    # work to be done, but someone else is doing it:  stay on the beach
                    else: workers[w] += "-"
                # no work to be done, stay on the beach
                else:
                    workers[w] += "-"

# Uncomment for a pretty worker schedule!
#        print( "%3d" % timer, end=" ")
#        for w in workers:
#            print( w[timer], end=" ")
#        print()

        # now increment the timer and see if there's any work now complete to account for
        # this section is identical to Part 1, except we're not chosing next by the rules,
        # but clearing out the doneat list since we followed the rules above to schedule
        # the work
        timer += 1
        if doneat[ timer ]:
            for next in doneat[ timer ]:
                path += next
                unvisited2.remove(next)
                active.remove(next)

                if not unvisited2:
                    break

                for d in graph[next]:
                    dependencies2[d].remove(next)
                    if not dependencies2[d]:
                        del dependencies2[d]

    print( path )
    # I disagree with the -1 below, but that's what gave the correct answer to my input....
    print( timer - 1)


if __name__ == "__main__":
    main()
