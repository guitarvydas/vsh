#!/bin/bash

set -e
trap 'catch' ERR

catch () {
    echo '*** FATAL ERROR in transpile.bash ***' 1>&2
    exit 1
}

# ./drawio2fb.bash

cdir=`pwd`
pfr $1.drawio drawio.ohm drawio.glue $cdir/support.js \
    | pfr - styleexpander.ohm styleexpander.glue $cdir/support.js \
    | pfr - attributeelider.ohm attributeelider.glue $cdir/support.js \
    | pfr - emitFactbase.ohm emitFactbase.glue $cdir/support.js \
    | sort >5.pl


## create rect fact for every vertex that is not an edge/ellipse/text
## sequence.drawio file contains vertexes, and marks all edge and ellipse (and text)
## but does not mark rectangles (the default)
## this pass finds the defaults and creates explicit rect(...) facts
swipl -q \
      -g 'consult(5).' \
      -g 'consult(rects).' \
      -g 'printRects.' \
      -g 'halt.' \
      > 6.pl

# augment the factbase (fb.pl) after every inferencing step
cat 5.pl 6.pl | sort >fb.pl

./run-queries.bash

