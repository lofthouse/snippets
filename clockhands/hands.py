#! /usr/bin/env python3

# h = hour
# m = minute
# hp = hour hand position (0-1, 1 = full revolution)
# mp = minute hand position (0-1, 1 = full revolution)
# error = maximum allowable error before we spit out a match

h = m = hp = mp = 0
error = 0.00000000001

# start at 00:00 and go until 12:00
while h < 12:
    # if the hands line up, pretty-print the time, then move the hour hand forward 1 hour
    if abs(hp-mp) < error:
        h = int(hp * 12)
        m = int(round(mp * 60,0))
        s = int(round(60 * (mp * 60 - m),0))

        # pesky negative seconds and whole minutes...
        if s < 0:
            s += 60
            m -= 1
        if m == 60:
            h += 1
            m = 0

        print( f"Match at {h}:{m:02d}:{s:02d}" )
        h += 1
        hp = h / 12
    # if they don't, advance the minute hand to where the hour hand was, then advance the hour hand
    else:
        mp = hp
        # this is the tricky bit:  mp is 0-1, and that's the portion of 1/12 a rotation that gets added to hp
        hp = (h/12 + mp/12)
