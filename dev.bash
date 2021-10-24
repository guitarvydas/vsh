#!/bin/bash
# node test.js

# node nbsp.js
# pfr nbsp.txt nbsp.ohm nbsp.action
# pfr nbsp.txt unhtml.ohm unhtml.action
# pfr create-rect-facts unhtml.ohm unhtml.action
# pfr create-rect-facts nbsp.ohm nbsp.action

./transpile.bash >7.json
names=`node emitBash.js`
# echo chmod a+x ${names}
chmod a+x ${names}

mydir=`pwd`
# pf - unhtml.ohm <run-queries

pfr run-queries unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
pfr create-rect-facts unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action

# pfr create-rect-facts unhtml.ohm unhtml.action >temp1
# cat temp1 | pfr - span.ohm span.action >temp2
# cat temp2

echo ${names}
pfr emit-bash unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
pfr permissions-to-execute unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
pfr sort-factbase unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
pfr drawio-to-factbase unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
pfr VSH unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action

#create-rect-facts

# for i in ${names}
# do
#     cat $i
# done >_all.html
