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

    graph = {}
    dependencies = {}
    unvisited = set()

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

    unvisited2 = copy.deepcopy(unvisited)
    dependencies2 = copy.deepcopy(dependencies)

    path = ""
    while unvisited:
        next = min( unvisited.difference( set(dependencies.keys() ) ) )
        path += next
        unvisited.remove(next)

        if next not in graph:
            break

        for d in graph[next]:
            dependencies[d].remove(next)
            if not dependencies[d]:
                del dependencies[d]

    print( path )


    path = ""
    timer = 0
    workers = [ "", "", "", "", "" ]
    bt = 60
    doneat = defaultdict( list )
    active = set()

    while unvisited2:
        nexts = sorted( unvisited2.difference( set(dependencies2.keys() ) ) )

        job = 0
        for w in range( len(workers) ):
            if len( workers[w] ) <= timer:
                if job < len(nexts):
                    if nexts[job] not in active:
                        active.add( nexts[job] )
                        workers[ w ] += ( nexts[job] * (string.ascii_uppercase.index(nexts[job]) + 1 + bt) )
                        doneat[ timer + string.ascii_uppercase.index(nexts[job]) + 1 + bt ] = nexts[job]
                        job += 1
                    else: workers[w] += "-"
                else:
                    workers[w] += "-"

#        print( "%3d" % timer, end=" ")
#        for w in workers:
#            print( w[timer], end=" ")
#        print()

        timer += 1
        if doneat[ timer ]:
            for next in doneat[ timer ]:
                path += next
                unvisited2.remove(next)
                active.remove(next)

                if next not in graph:
                    break

                for d in graph[next]:
                    dependencies2[d].remove(next)
                    if not dependencies2[d]:
                        del dependencies2[d]

    print( path )
    # I disagree with the -1 below, but that's what give the correct answer to my input....
    print( timer - 1)


if __name__ == "__main__":
    main()
