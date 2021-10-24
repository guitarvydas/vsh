#!/bin/bash
# node test.js
./transpile.bash >7.json
names=`node emitBash.js`
# echo chmod a+x ${names}
chmod a+x ${names}

mydir=`pwd`
# pf run-queries unhtml.ohm
pfr run-queries unhtml.ohm identity-unhtml.action

# pfr temp1 span.ohm span.action >temp2
# pfr temp2 para.ohm para.action

#create-rect-facts

# for i in ${names}
# do
#     cat $i
# done >_all.html
