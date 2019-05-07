#! /usr/bin/env python3

# h = hour
# m = minute
# hp = hour hand position (0-1, 12ths of a revolution)
# mp = minute hand position (0-1, 12ths of a revolution)
# error = maximum allowable error before we spit out a match

h = m = hp = mp = 0
error = 0.000000000001

# start at 00:00 and go until 12:00
while h < 12:
    # if the hands line up, pretty-print the time, then move the hour hand forward 1 hour
    if abs(hp-mp) < error:
        h = int(hp * 12)
        m = int(mp * 60)
        s = 60 * (mp * 60 - m)
        print( f"Match at {h}:{m}:{s}" )
        h += 1
        hp = h / 12
    # if they don't, advance the minute hand to where the hour hand was, then advance the hour hand
    else:
        mp = hp
        hp = (h/12 + mp/60)
