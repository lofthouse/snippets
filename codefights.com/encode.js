encode = s => {
    o='';
    l=s[0];
    for(c=i=1;i<=s.length;i++) {
        if(s[i]==l)
            c++;
        else {
            o+=l+c;
            l=s[i];
            c=1;
        }
    }
    return o;
}
