#! /usr/bin/env python3
import os
import sys
import networkx as nx

### HI TREVOR!
# the below kinda really did not work, but was a valiant effort
# you need to redo this as a graph (use nx!) then you can simply call shortest_path_length(graph,origin,destination)

moves = {'N':(0,1), 'E':(1,0), 'S':(0,-1), 'W':(-1,0) }

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

# takes in the regex to work on and adds all found routes to the master graph
# starting from origin.  Returns the index of the end of the parsable section
# (e.g. when it ran into a closing ')' it didn't start
def parse( input_str, origin, in_paren ):
#    print( "Starting a",n,"-level parse of",input_str)

    i = 0
    this_room = origin

    while i < len(input_str):
        if input_str[i] == '(':
            count = parse( input_str[(i+1):], this_room, True )
            i += count + 1

        elif input_str[i] == '|':
            count = parse( input_str[(i+1):], origin, in_paren )
            i += count

        elif input_str[i] == '$' or ( in_paren and input_str[i] == ')' ):
            i += 1
            return i

        # this case ... shouldn't exist?
        elif input_str[i] == '^' or input_str[i] == ')':
            i += 1

        else:
            new_room = tuple( [ a+b for a,b in zip(this_room,moves[ input_str[i] ]) ] )
            graph.add_edge( this_room, new_room )
            this_room = new_room

            i += 1

def main():
    regexes = readfile()

    for regex in regexes:
        global graph
        graph = nx.Graph()

        #regex starts with a '^', so we only care about 1: slice
        parse( regex[1:], (0,0), 0 )
        print( "Parsing complete" )

        furthest_node = ''
        furthest_path = 0
        path_over_1000 = 0

        for node in graph.nodes:
            print( "Calculating path to", node, "...\r", end='' )
            this_path = nx.shortest_path_length(graph,(0,0),node)

            if this_path > furthest_path:
                furthest_path = this_path
                furthest_node = node

            if this_path >= 1000:
                path_over_1000 += 1

        print( "The shortest longest path is", furthest_path, "to reach", furthest_node )
        print( "There are", path_over_1000, "rooms at least 1000 doors away" )

if __name__ == "__main__":
    main()
