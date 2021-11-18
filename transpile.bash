#!/bin/bash

set -e
trap 'catch' ERR

catch () {
    echo '*** FATAL ERROR in transpile.bash ***' 1>&2
    exit 1
}

../d2j/d2j $1

cp fb.pl _r2.pl
 
./run-queries.bash

