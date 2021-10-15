#!/bin/bash
cdir=`pwd`
pfr vsh.drawio drawio.ohm drawio.action $cdir/support.js >1.txt
pfr 1.txt styleexpander.ohm styleexpander.action $cdir/support.js >2.txt
pfr 2.txt attributeelider.ohm attributeelider.action $cdir/support.js >3.txt
#pfr 3.txt nametable.ohm nametable.action $cdir/support.js >4.txt
pfr 3.txt emitFactbase.ohm emitFactbase.action $cdir/support.js >5.txt
sort <5.txt >6.pl
