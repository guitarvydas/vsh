#!/bin/bash
./transpile.bash >7.json
names=`node emitBash.js 7.json`
# echo chmod a+x ${names}
# chmod a+x ${names}

pfr drawio-to-factbase unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh-boot/drawio-to-factbase
pfr create-rect-facts unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh-boot/create-rect-facts
pfr sort-factbase unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh-boot/sort-factbase
pfr run-queries unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh-boot/run-queries
pfr emit-bash unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh-boot/emit-bash
pfr permissions-to-execute unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh-boot/permissions-to-execute
pfr make_vsh unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw >../vsh-boot/make_vsh

chmod a+x ../vsh-boot/drawio-to-factbase ../vsh-boot/create-rect-facts ../vsh-boot/sort-factbase ../vsh-boot/run-queries ../vsh-boot/emit-bash ../vsh-boot/permissions-to-execute
ls -l ../vsh-boot
