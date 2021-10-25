#!/bin/bash
./transpile.bash >7.json
names=`node emitBash.js 7.json`
# echo chmod a+x ${names}
# chmod a+x ${names}

pfr drawio_to_factbase unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh_boot/drawio_to_factbase
pfr create_rect_facts unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh_boot/create_rect_facts
pfr sort_factbase unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh_boot/sort_factbase
pfr run_queries unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh_boot/run_queries
pfr emit_bash unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh_boot/emit_bash
pfr permissions_to_execute unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh_boot/permissions_to_execute
pfr make_vsh unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh_boot/make_vsh

chmod a+x ../vsh_boot/drawio_to_factbase ../vsh_boot/create_rect_facts ../vsh_boot/sort_factbase ../vsh_boot/run_queries ../vsh_boot/emit_bash ../vsh_boot/permissions_to_execute ../vsh_boot/make_vsh
ls -l ../vsh_boot
