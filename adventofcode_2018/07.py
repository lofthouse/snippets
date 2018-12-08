#! /usr/bin/env python3
import os
import sys

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


if __name__ == "__main__":
    main()
