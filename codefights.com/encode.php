function encode($s) {
    for($i=0;$i<strlen($s);$i++) {
        if($s[$i]==$l)
            $c++;
        else {
            if($c)
                $o .= $l . $c;
            $l=$s[$i];
            $c=1;
        }
    }
    return $o . $l . $c;
}
