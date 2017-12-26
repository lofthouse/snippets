#!/usr/bin/env python
import sys
import os

rows = 0
cols = 0

def debug(*args):
    if 'DEBUG' in os.environ:
        print " ".join(map(str,args))

def getArgs():
    if len(sys.argv) != 3 :
        print "Invalid argument"
        print "%s <input file> <part>" % sys.argv[0]
        sys.exit(1)

    if os.path.isfile(sys.argv[1]):
        with open(sys.argv[1]) as input_file:
            input = input_file.read().splitlines()
            maze = map(list,input)
    else:
        print "%s is not a file" % sys.argv[1]
        sys.exit(1)

    return maze

# Begin actual code

def findMove(move,position,maze):
    response = None

    # if we're moving across a row, look up and down
    if move[0] == 0:
        candidates = [ [1,0], [-1,0] ]
    else:
        candidates = [ [0,1], [0,-1] ]

    debug( "Finding a move!" )

    for candidate in candidates:
        row,col = [ sum(i) for i in zip(position,candidate) ]

        if 0 <= row and row < rows and 0 <= col and col < cols:
            try:
                debug( "Trying [",row,",",col,"]" )
                if maze[row][col] != ' ':
                    if response is not None:
                        print "ERROR:  two paths found!"
                        printMaze(maze)
                        sys.exit(1)
                    else:
                        debug( "WINNER" )
                        response = candidate
            except:
                # out of bounds!
                pass

    return response

def findStart(maze):
    for col in range(cols):
        if maze[0][col] == '|':
            return [0,col]

def printMaze(maze):
    for line in maze:
        print ''.join(line)

def main():
    maze = getArgs()
    global rows
    global cols

    rows = len(maze)
    cols = len(maze[0])

    position = findStart(maze)

    move = [1,0]
    sequence = ""
    steps = 0

    while move is not None:
        position = [ sum(i) for i in zip(position,move) ]
        steps = steps + 1

        row,col = position
        segment = maze[row][col]
        maze[row][col] = '#'

        if segment == '+':
            move = findMove(move,position,maze)
        if segment.isalpha():
            sequence = sequence + segment
        if segment == ' ':
            break

    print sequence
    print "That took %d steps" % steps

if __name__=='__main__':
    main()
