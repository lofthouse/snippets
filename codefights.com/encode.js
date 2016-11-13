encode = s => {
    o=''
    i=0
    while (i<s.length) {
        c=1
        while(s[i]==s[i+c])
                c++
            o+=s[i]+c
            i+=c
    }
    return o
}
