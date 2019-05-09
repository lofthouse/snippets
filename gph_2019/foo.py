#!/usr/bin/env python3

import string
import heapq

def bowser(input):
    lowest = sorted( input )[0]
    return input.replace(lowest,'')

def red(input):
    temp = input.replace("L","#")
    temp = temp.replace("R","L")
    return temp.replace("#","R")

def boo(input):
    vowels = "UAEIOUA"
    output = ""

    for c in input:
        if c in vowels:
            i = vowels.find(c,1)
            output += vowels[i-1] + vowels[i+1]
        else:
            output += c

    return output

def doggy(input,n):
    alphabet = "Z" + string.ascii_uppercase + "A"
    i = alphabet.find(input[n],1)

    return ( input[0:n] + alphabet[i+1] + alphabet[i-1] + input[n+1:] )

def ghost(input,c):
    return ( input[0] + c + input[1:-2] + c + input[-1] )

def cloud(input,n):
    return ( input[n:] + input[:n] )


def test():
    input="ABCD"

    print( "Bowser:" )
    print( bowser(input) )
    print( )
    print( "Red:" )
    print( red(input) )
    print( )
    print( "Boo:" )
    print( boo(input) )
    print( )
    print( "Doggy:" )
    print( doggy(input,0) )
    print( doggy(input,1) )
    print( doggy(input,2) )
    print( doggy(input,3) )
    print( )
    print( "Ghost:" )
    print( ghost(input,"Z") )
    print( )
    print( "Cloud:" )
    print( cloud(input,0) )
    print( cloud(input,1) )
    print( cloud(input,2) )
    print( cloud(input,3) )

def main():
    q = []
    heapq.heapify( q )

    tried = set()

    start = "SHRINE"
    finish = "REFRESHROOM"
    candidate = start
    longest = 0
    n = 0
    steps = ""
#    heapq.heappush( q, (0,start,"") )

    while( candidate != finish ):
        if candidate not in tried:
            tried.add(candidate)
            if n > longest:
                longest = n
                print( "Trying %d step solutions" % n )

            heapq.heappush( q, (n+1,bowser(candidate),steps+"Bowser,") )
            heapq.heappush( q, (n+1,red(candidate),steps+"Red,") )
            heapq.heappush( q, (n+1,boo(candidate),steps+"Boo,") )

            for i in range(len(candidate)):
                heapq.heappush( q, (n+1,doggy(candidate,i),steps+"Doggy(%d),"%i) )

            for c in set( candidate ):
                heapq.heappush( q, (n+1,ghost(candidate,c),steps+"Ghost(%s),"%c) )

            for i in range(len(candidate)):
                heapq.heappush( q, (n+1,cloud(candidate,i),steps+"Cloud(%d),"%i) )

        n,candidate,steps = heapq.heappop(q)

    print( "Finished in %d steps by doing %s" % (n,steps) )

if __name__ == "__main__":
    main()
