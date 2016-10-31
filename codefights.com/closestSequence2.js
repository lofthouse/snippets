function closestSequence2(a, b) {
    var a_len=a.length;
    var b_len=b.length;
    var i=0;
    var j=0;
    var diff_table=[];
    var diff=0;

    for (k=0; k<=a_len; k++)
        diff_table[k]=[];
    for (k=0; k<=b_len; k++)
        diff_table[0][k]=0;

    for (i=1; i<=a_len; i++) {
        for (j=i; j<=b_len; j++) {
            diff=Math.abs(b[j-1]-a[i-1]);
            if (i == j)
                diff_table[i][j]=diff+diff_table[i-1][j-1];
            else
                diff_table[i][j]=Math.min(diff_table[i][j-1],diff_table[i-1][j-1]+diff);
        }
    }
    return diff_table[a_len][b_len];
}
