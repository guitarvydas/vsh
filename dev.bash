#!/bin/bash
# node test.js
./transpile.bash >7.json
names=`node emitBash.js`
# echo chmod a+x ${names}
chmod a+x ${names}

mydir=`pwd`
pf - unhtml.ohm <run-queries

# pfr run-queries unhtml.ohm unhtml.action >temp1
# pfr - span.ohm span.action <temp1 >temp2
# pfr temp2 para.ohm para.action

#create-rect-facts
# pfr create-rect-facts unhtml.ohm unhtml.action >temp1
# pfr temp1 span.ohm span.action >temp2
# pfr temp2 para.ohm para.action

# for i in ${names}
# do
#     cat $i
# done >_all.html
