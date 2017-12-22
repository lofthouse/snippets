#!/usr/bin/env python
import sys
import os.path
import networkx as nx

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

def main():
    input = getArgs()
    G = nx.Graph()

    # line format:  1976 <-> 872, 1310, 1565, 1637
    for line in input:
        pieces = line.split()

        here = pieces[0]
        G.add_node(here)

        theres = [ x.strip(',') for x in pieces[2:] ]

        for there in theres:
            G.add_edge(here,there)

    print "There are %d nodes reachable from 0" % (len( nx.descendants(G,"0") ) + 1)

    print "There are %d groups" % len( list(nx.connected_components(G)) )

if __name__=='__main__':
    main()
