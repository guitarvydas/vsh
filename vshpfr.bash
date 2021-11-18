#!/bin/bash

set -e
trap 'catch' ERR

catch () {
    exit 1
}

# usage: pf source-file grammar-file rewrite-file
pdir=~/quicklisp/local-projects/pfr
support=$4
tflag=$5
vflag=$6
node $pdir/parse.js $1 $2 $3 $support $tflag $vflag
