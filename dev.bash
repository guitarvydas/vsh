#!/bin/bash
# node test.js
# node nbsp.js
./transpile.bash >7.json
names=`node emitBash.js`
# echo chmod a+x ${names}
chmod a+x ${names}

mydir=`pwd`
# pf - unhtml.ohm <run-queries

# pfr run-queries unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action
# pfr create-rect-facts unhtml.ohm unhtml.action | pfr - span.ohm span.action | pfr - para.ohm para.action

pfr create-rect-facts unhtml.ohm unhtml.action >temp1
cat temp1 | pfr - span.ohm span.action >temp2

#create-rect-facts

# for i in ${names}
# do
#     cat $i
# done >_all.html
