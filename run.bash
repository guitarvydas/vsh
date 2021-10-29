#!/bin/bash
clear

set -e
trap 'catch' ERR

catch () {
    echo '*** FATAL ERROR in run.bash ***'
    exit 1
}

./transpile.bash async_helloworld >7.json
names=`node emitBash.js 7.json`
# echo chmod a+x ${names}
# chmod a+x ${names}

echo

for i in $names
do
    echo processing $i
    mv $i orig_$i
    pfr orig_$i unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue | pfr - font.ohm font.glue >$i
    chmod a+x $i 
done
