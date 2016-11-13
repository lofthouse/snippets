def encode(s):
    o = ''
    c = 0
    l = s[0]
    for x in s:
        if x == l:
            c += 1
        else:
            o += l + str(c)
            l = x
            c = 1
    return o + l + str(c)
