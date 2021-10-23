#!/bin/bash
./transpile.bash
names=`node emitBash.js`
echo chmod a+x ${names}
chmod a+x ${names}
# echo
# echo '*** running VSH0 ***'
# ./VSH0
