#! /usr/bin/env python3
import os
import sys

def readfile():
    if len(sys.argv) != 2 or not os.path.isfile( sys.argv[1] ):
        print( f"Usage:  {sys.argv[0]} <input_file>" )
        sys.exit(1)

    with open( sys.argv[1] ) as in_file:
        return in_file.read().splitlines()

def parse( input_str, n ):
#    print( "Starting a",n,"-level parse of",input_str)

    i = 0
    out = [ "" ]

    while i < len(input_str):
#        print( "Outs are now", out )
#        print( "Now looking at", input_str[i], input_str )
#        input()

        if input_str[i] == '(':
            count,sub = parse( input_str[(i+1):], 1 )

            # if there are any 0-length options, this does not add a shortest path!  IGNORE
            if len( min(sub, key=len) ) > 0:
#                print( "mixing", out, "and", sub )

                new_leg = max(sub, key=len)
                for j in range( len(out) ):
                    out[j] += new_leg
#                for j in range( len(out) ):
#                    for s in sub:
#                        out[j] += s
#            else:
#                print( "Skipping mix:  0-length path!" )
            i += count + 1
        elif input_str[i] == '|':
            count,sub = parse( input_str[(i+1):], n )
            for j in range( len(out) ):
                for s in sub:
                    out.append(s)
            i += count
        elif input_str[i] == '$' or ( n>0 and input_str[i] == ')' ):
            i += 1
#            print( "Returning", (i,out) )
            return (i,out)
        elif input_str[i] == '^' or input_str[i] == ')':
            i += 1
        else:
            for j in range( len(out) ):
                out[j] += input_str[i]
            i += 1

def main():
    regexes = readfile()

    for regex in regexes:
        null,routes = parse( regex[1:], 0 )

        print( routes )
        print( "The shortest longest path is", len( max(routes, key=len) ) )

if __name__ == "__main__":
    main()
