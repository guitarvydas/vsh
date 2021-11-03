#!/bin/bash
cdir=`pwd`
# pfr vsh.drawio drawio.ohm drawio.glue $cdir/support.js >1.txt
# pfr 1.txt styleexpander.ohm styleexpander.glue $cdir/support.js >2.txt
# pfr 2.txt attributeelider.ohm attributeelider.glue $cdir/support.js >3.txt
# pfr 3.txt emitFactbase.ohm emitFactbase.glue $cdir/support.js >4.txt
# sort <4.txt >5.pl


pfr vsh.drawio drawio.ohm drawio.glue $cdir/support.js \
    | pfr 1.txt styleexpander.ohm styleexpander.glue $cdir/support.js \
    | pfr 2.txt attributeelider.ohm attributeelider.glue $cdir/support.js \
    | pfr 3.txt emitFactbase.ohm emitFactbase.glue $cdir/support.js \
    | sort >5.pl
