#! /usr/bin/env python3
import os
import sys
from numpy import array, zeros, array_equal

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        lines = in_file.read().splitlines()


    w = len(lines[0])
    h = len(lines)
    map = zeros( (h+2, w+2), dtype=int )

    for r,line in enumerate(lines):
        for c,char in enumerate(line):
            if char == '|':
                map[r+1][c+1] = 1
            if char == '#':
                map[r+1][c+1] = 8

    return (map,h,w)

def mapprint( map, rows, cols ):
    for j in range(1,rows+1):
        for i in range(1, cols+1):
            if map[j][i] == 0:
                print('.',end='')
            elif map[j][i] == 1:
                print('|',end='')
            elif map[j][i] == 8:
                print('#',end='')
        print()

def tick( map,rows,cols ):
    new_map = zeros( (rows+2, cols+2), dtype=int )

    for j in range(1,rows+1):
        for i in range(1,cols+1):
            # 3 adjacent trees seeds an open
            if map[j][i] == 0:
                if (map[j-1:j+2,i-1:i+2] == 1).sum() >= 3:
                    new_map[j][i] = 1
            # 3 adjacent lumberyards develops a tree
            elif map[j][i] == 1:
                if (map[j-1:j+2,i-1:i+2] == 8).sum() >= 3:
                    new_map[j][i] = 8
                else:
                    new_map[j][i] = 1
            # sawmills need at least one tree and sawmill adjacent to survive
            elif map[j][i] == 8:
                # WARNING: don't count yourself as a neighboring sawmill!!!  strictly > 1 test, not >= 1
                if ( (map[j-1:j+2,i-1:i+2] == 1).sum() >= 1 ) and ( (map[j-1:j+2,i-1:i+2] == 8).sum() > 1 ):
                    new_map[j][i] = 8
                else:
                    new_map[j][i] = 0
            else:
                print( "LOGIC ERROR" )
                exit( -1 )

    return new_map

def main():
    map,rows,cols = readfile()
    states = set()
    maps = []
    p2_finished = False

    for i in range(1000000000):
        if p2_finished:
            shadow_i += 1
            if shadow_i == cycle_rpt:
                shadow_i = cycle_bot
        else:
            map = tick( map,rows,cols )
            hash = ''.join(''.join(str(c) for c in r) for r in map)

            if hash in states:
                print( "Repeat found at index", i )

                for j,saved_map in enumerate(maps):
                    if array_equal(saved_map,map):
                        print( "Run index",j,"and index",i,"were the same")
                        break

                cycle_bot=j
                cycle_rpt=i
                cycle = (i-j+1)
                shadow_i = j

                x = j + ( (1000000000-j) % cycle )
                print( "Winner should be around",x )
                p2_finished = True
            else:
                states.add( hash )
                maps.append( map )

            if i == 9:
                trees = (map == 1).sum()
                yards = (map == 8).sum()

                print( "Trees:", trees )
                print( "Yards:", yards )
                print( "Score:", trees*yards )

#        if p2_finished:
#            for z in range(j,i):
#                print("Showing map stored at",z)
#
#                map = maps[z]
#                trees = (map == 1).sum()
#                yards = (map == 8).sum()
#
#                print( "Trees:", trees )
#                print( "Yards:", yards )
#                print( "Score:", trees*yards )
#                print()
#            break

    print( "Shadow_i=",shadow_i )

if __name__ == "__main__":
    main()
