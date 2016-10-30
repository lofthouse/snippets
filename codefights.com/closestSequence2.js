function closestSequence2(a, b) {
    var len=a.length;
    var i=0;
    var b_prime=[];

    if (b.length == len) {
        return diff(a,b);
    } else {
        var min=0;
        var min_candidate=0;

        for (i=0; i<b.length; i++) {
            var head=b.slice(0,i);
            var tail=b.slice(i+1,b.length);
            var b_prime_candidate=head.concat(tail);
            if (i == 0) {
                min=closestSequence2(a,b_prime_candidate);
                b_prime=b_prime_candidate;
            } else {
                min_candidate=closestSequence2(a,b_prime_candidate);
                if( min_candidate<min ) {
                    min=min_candidate;
                    b_prime=b_prime_candidate;
                }
            }
        }
        return min;
    }
}

function diff(a,b) {
    var sum=0;
    var i=0;

    for (i=0; i<a.length; i++) {
        sum+=Math.abs(a[i]-b[i]);
    }
    return sum;
}
