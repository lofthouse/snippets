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

def findBalance( node, imbalance ):
    max_load = 0

    if len(node.children) > 0:
        weights = set()

        for child in node.children:
            load = getBalance(child)
            weights.add(load)

            if load > max_load:
                max_load = load
                max_child = child

        new_imbalance = max(weights) - min(weights)

        if new_imbalance > 0:
            print "I'm %s weighing %d and it appears that child %s is over by %d" % (node.name, node.weight, max_child.name, new_imbalance)
            findBalance( max_child, new_imbalance )
        else:
            print "I'm %s and I'm the culprit!  I should actually weigh %d." % ( node.name, node.weight - imbalance )

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

    print "The root of the tree is %s" % root.name
    findBalance( root, 0 )


if __name__=='__main__':
    main()
