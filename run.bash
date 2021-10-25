#!/bin/bash
./transpile.bash >7.json
names=`node emitBash.js`
echo chmod a+x ${names}
chmod a+x ${names}

pfr drawio-to-factbase unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw
pfr create-rect-facts unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw
pfr sort-factbase unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw
pfr run-queries unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw
pfr emit-bash unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw
pfr permissions-to-execute unhtml.ohm unhtml.srw | pfr - span.ohm span.srw | pfr - para.ohm para.srw | pfr - div.ohm div.srw

# echo
# echo '*** running VSH0 ***'
# ./VSH0
