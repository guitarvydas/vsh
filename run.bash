#!/bin/bash
./transpile.bash >7.json
names=`node emitBash.js 7.json`
# echo chmod a+x ${names}
# chmod a+x ${names}

pfr drawio_to_factbase unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/boot_drawio_to_factbase
pfr create_rect_facts unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/boot_create_rect_facts
pfr sort_factbase unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/boot_sort_factbase
pfr run_queries unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/boot_run_queries
pfr emit_bash unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/boot_emit_bash
pfr permissions_to_execute unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/boot_permissions_to_execute
pfr make_vsh unhtml.ohm unhtml.glue | pfr - span.ohm span.glue | pfr - para.ohm para.glue | pfr - div.ohm div.glue >../vsh_boot/boot_make_vsh

chmod a+x ../vsh_boot/boot_drawio_to_factbase ../vsh_boot/boot_create_rect_facts ../vsh_boot/boot_sort_factbase ../vsh_boot/boot_run_queries ../vsh_boot/boot_emit_bash ../vsh_boot/boot_permissions_to_execute ../vsh_boot/boot_make_vsh
