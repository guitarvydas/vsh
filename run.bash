#!/bin/bash
clear

target=helloworld
#target=transpile_drawio_to_swipl

set -e
trap 'catch' ERR

catch () {
    echo '*** FATAL ERROR in run.bash ***'
    exit 1
}

#./transpile.bash async_helloworld >7.json
./transpile.bash $target >7.json
names=`node emitBash.js 7.json`
# echo chmod a+x ${names}
# chmod a+x ${names}

echo

for i in $names
do
    echo processing $i
    mv $i orig_$i
    ./vshpfr.bash orig_$i unhtml.ohm unhtml.glue | ./vshpfr.bash - span.ohm span.glue | ./vshpfr.bash - para.ohm para.glue | ./vshpfr.bash - div.ohm div.glue | ./vshpfr.bash - font.ohm font.glue | ./vshpfr.bash - unhtml2.ohm unhtml2.glue >$i
    chmod a+x $i 
done

echo
echo '*** running result ***'
echo
./$target $target
