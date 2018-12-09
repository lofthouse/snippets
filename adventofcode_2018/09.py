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
    for game in readfile():
        players,_,_,_,_,_,marbles,_ = game.split()
        players = int(players)
        marbles = int(marbles)

        circle = [ 0 ]
        scores = [ 0 for i in range(players) ]
        turn = 0
        current = 0
        for marble in range(1,marbles+1):
            if marble % 23 == 0:
                scores[ turn ] += marble + circle[ (current - 7) % len(circle) ]
                circle.pop( (current - 7) % len(circle) )
                current = ( ( current - 7 ) % ( 1 + len(circle) ) ) % len(circle)
            else:
                circle.insert( (current + 1) % len(circle) + 1, marble )
                current = ( current + 1 ) % ( len(circle) - 1 ) + 1
            turn = (turn + 1) % players

        print( max(scores) )
if __name__ == "__main__":
    main()
