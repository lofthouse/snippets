#! /usr/bin/env python3

h = m = hp = mp = 0
error = 0.000000000001

while h < 12:
    if abs(hp-mp) < error:
        h = int(hp * 12)
        m = int(mp * 60)
        s = 60 * (mp * 60 - m)
        print( f"Match at {h}:{m}:{s}" )
        h += 1
        hp = h / 12
    else:
        mp = hp
        hp = (h/12 + mp/60)
#        print( f"Trying {int(hp * 12)}:{mp * 60}" )
