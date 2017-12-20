#!/usr/bin/env python
import sys
import os.path
from anytree import Node, RenderTree

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

def printBalance( node ):
    max_load = 0

    if len(node.children) > 0:
        for child in node.children:
            load = getBalance(child)

            if load > max_load:
                max_load = load
                max_child = child

            print "I'm %s weighing %d and child %s has %d" % ( node.name, node.weight, child.name, getBalance(child) )

        printBalance( max_child )

def getBalance( node ):
    if node.children == None:
        return 0
    else:
        return node.weight + sum(map(getBalance,node.children))

def main():
    input = getArgs()
    nodes = {}

    for line in input:
        pieces = line.split()
        me = pieces[0]
        weight = int( pieces[1].strip('()') )

        # node already created, just update weight
        if me in nodes:
            nodes[ me ].weight = weight
        else:
            nodes[ me ] = Node( me, weight = weight )

        # do we have a child list?
        if len(pieces) > 2:
            children = [ x.strip(',') for x in pieces[3:] ]

            for child in children:
                if child in nodes:
                    nodes[ child ].parent = nodes[ me ]
                else:
                    nodes[ child ] = Node( child, weight = 0, parent = nodes[ me ] )

    root = nodes[ me ].root

    print( root )

    printBalance( root )



if __name__=='__main__':
    main()
