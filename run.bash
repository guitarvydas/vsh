#!/bin/bash
clear

set -e
trap 'catch' ERR

catch () {
    echo '*** FATAL ERROR in run.bash ***'
    exit 1
}

./transpile.bash helloworld >7.json
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

# pfr drawio_to_factbase unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/drawio_to_factbase
# pfr create_rect_facts unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/create_rect_facts
# pfr sort_factbase unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/sort_factbase
# pfr run_queries unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/run_queries
# pfr emit_bash unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/emit_bash
# pfr permissions_to_execute unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/permissions_to_execute
# pfr unhtml unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue | pfr - font.ohm font.glue >../vsh_boot/unhtml
# pfr make_vsh unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/make_vsh

