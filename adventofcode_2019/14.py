#! /usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(description='Advent of Code 2019 Day N')
parser.add_argument('input_file', type=argparse.FileType('r'))
parser.add_argument("-v", "--verbose", help="Include (useful) debug messages",action="store_true")
#parser.add_argument("x", type=int, help="the number x")
args = parser.parse_args()

def readfile():
    with args.input_file as input_file:
        return input_file.read().splitlines()

# each ing entry will look like:
# 'A': [10, [[10, 'ORE']]]
# or
#   yield from [[qty,input],...]
# 'E': [1, [[7, 'A'], [1, 'D']]
def ore_to_make( target, qty, reactions, balances ):
    ore_counts = 0

    if args.verbose:
        print( "Figuring out how to make", qty, target )

    makes, ingredients = reactions[ target ]
    # If we need 1, but the recipe makes 10, we have to make 10
    # Hat-Tip to poke:  https://stackoverflow.com/questions/14822184/is-there-a-ceiling-equivalent-of-operator-in-python
    mult = (qty + ( makes - 1 ) ) // makes
    if args.verbose:
        print( "I will need use", mult, "copies of the recipe" )

    for ing in ingredients:
        need = ing[ 1 ]
        ing_count = mult * ing[ 0 ]
        on_hand = 0
        ore_count = 0

        if need != 'ORE':
            if need in balances:
                on_hand = balances[ need ]
                if args.verbose:
                    print( "turns out I already have", balances[ need ] )

            if on_hand < ing_count:
                if on_hand > 0:
                    balances[ need ] -= on_hand
                ore_count,balances = ore_to_make( need, ing_count - on_hand, reactions, balances )
                balances[ need ] -= (ing_count - on_hand)
            else:
                balances[ need ] -= ing_count
                ore_count = 0
        else:
            ore_count = ing_count

        ore_counts += ore_count

    if target in balances:
        balances[ target ] += mult * makes
    else:
        balances[ target ] = mult * makes

    if args.verbose:
        print( "Needed a net of", ore_counts, "ore to make", qty, target )
        print( balances )

    return ore_counts,balances

def main():
    lines = readfile()

    reactions = {}
    balances = {}

    for line in lines:
        in_list,out = line.split(' => ')
        out_count,out_name = out.split()

        in_pieces = in_list.split(', ')

        in_list = []
        for piece in in_pieces:
            temp = piece.split()

            in_list.append( [ int( temp[0] ), temp[1] ] )

        reactions[ out_name ] = [ int( out_count), in_list ]

    print( ore_to_make( 'FUEL', 1, reactions, balances ) )


if __name__ == "__main__":
    main()
