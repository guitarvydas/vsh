#!/bin/bash

set -e
trap 'catch' ERR

catch () {
    echo '*** FATAL ERROR in run-queries.bash ***' 1>&2
    exit 1
}

./run.bash
./transpile_drawio_to_swipl helloworld
