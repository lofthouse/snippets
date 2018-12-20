#! /usr/bin/env python3
import os
import sys

def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print( f"Usage:  {sys.argv[0]} <recipe count>" )
        sys.exit(1)

    count = int( sys.argv[1] )
    search = [ i for i in sys.argv[1] ]
    search_key = 0
    search_length = len(search)

    e1 = 0
    e2 = 1

    recipes = [3,7]
    l = 2
    lim = count + 10

    part1 = False
    part2 = False

    while (not part1 or not part2):
        if search_key == 0:
            recipe_count = l

        in_list_count = 0

        for x in list(str( recipes[e1] + recipes[e2] )):
            if not part2:
                in_list_count += 1
                if x != search[ search_key ]:
                    search_key = 0
                    recipe_count += in_list_count

                if x == search[ search_key ]:
                    search_key += 1
                    if search_key == search_length:
                        print( f"Part 2: {recipe_count}" )
                        part2 = True
                        search_key = 0
                else:
                    search_key = 0
            recipes.append( int(x) )


        l = len(recipes)
        e1 = (e1 + 1 + recipes[e1]) % l
        e2 = (e2 + 1 + recipes[e2]) % l

        if not part1 and l >= lim:
            part1 = True
            print( "Part 1:", ''.join( [ str(i) for i in recipes[count:count+10] ] ) )

if __name__ == "__main__":
    main()
