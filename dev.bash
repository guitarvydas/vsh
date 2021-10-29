#!/bin/bash

set -e
trap 'catch' ERR

catch () {
    echo '*** FATAL ERROR in run-queries.bash ***' 1>&2
    exit 1
}

# convert fb.pl to JSON form
swipl -g 'use_module(library(http/json))' \
      -g 'consult(fb).' \
      -g 'consult(component).' \
      -g 'consult(names).' \
      -g 'consult(code).' \
      -g 'consult(jsoncomponent).'\
      -g 'allc.'
