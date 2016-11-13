function encode($s) {
    while ($i<strlen($s)) {
        $c=1;
        while($s[$i]==$s[$i+$c])
                $c++;
            $o .= $s[$i] . $c;
            $i += $c;
    }
    return $o;
}
