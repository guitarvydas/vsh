#!/bin/bash

set -e
trap 'catch' ERR

catch () {
    echo '*** FATAL ERROR in run-queries.bash ***' 1>&2
    exit 1
}

echo
echo '*** run.bash ***'
./run.bash
echo
echo '*** transpile_drawio_to_swipl ***'
./transpile_drawio_to_swipl helloworld

# echo
# echo '*** pfr orig_bounding_boxes ***'
# pfr orig_bounding_boxes unhtml.ohm unhtml.glue
