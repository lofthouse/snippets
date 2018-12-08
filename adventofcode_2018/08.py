#! /usr/bin/env python3
import os
import sys

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()[0]

# returns the value,total length, and summed metadata for the node and all embedded children
def mdsum( data ):
    children = data[0]
    md = data[1]

    # offset will record the total length of the node and all embeds:  it's at least 2 and we'll add
    # to it as we resolve any children
    offset = 2
    md_sums = 0
    value = 0
    # child_values will store the values from each child in order so we can compute our own value later
    child_values = []
    for i in range( children ):
        v,l,s = mdsum( data[offset:-md])
        child_values.append(v)
        offset += l
        md_sums += s

    if children == 0: # value is simply the sum or our metadata:  they start at the offset we've found
        value = sum( data[ offset:offset + md ] )
    else: # value is the sum of each named child's value, if it exists
        for child in data[ offset:offset + md ]:
            # children are 1-indexed;  boooo!
            if child - 1 < len( child_values ):
                value += child_values[ child - 1 ]

    return ( value, offset + md, md_sums + sum( data[ offset:offset + md ] ) )

def main():
    data = [ int(i) for i in readfile().split() ]

    value, length, sum = mdsum( data )
    print( f"The sum of the metadata is {sum}")
    print( f"The value of the root note is {value}")

if __name__ == "__main__":
    main()
