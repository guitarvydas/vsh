#!/bin/bash
./transpile.bash >7.json
names=`node emitBash.js`
echo chmod a+x ${names}
chmod a+x ${names}

pfr drawio-to-factbase unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
pfr create-rect-facts unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
pfr sort-factbase unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
pfr run-queries unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
pfr emit-bash unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
pfr permissions-to-execute unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action

# echo
# echo '*** running VSH0 ***'
# ./VSH0
