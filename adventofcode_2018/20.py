#! /usr/bin/env python3
import os
import sys
import networkx as nx

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

        paths = nx.shortest_path_length( graph, (0,0) )
        print( "The shortest longest path is", max( paths.values() ) )
        print( "There are", sum( [ 1 for i in paths.values() if i >= 1000 ] ), "rooms at least 1000 doors away" )

if __name__ == "__main__":
    main()
