#!/bin/bash
clear

target=helloworld

set -e
trap 'catch' ERR

catch () {
    echo '*** FATAL ERROR in run.bash ***'
    exit 1
}

d2f $target.drawio >fb.pl
f2j <fb.pl >${target}.json

echo

for i in helloworld hello world
do
    echo processing $i
    mv $i orig_$i
    pfrs orig_$i unhtml.ohm unhtml.glue nosupport.js \
	| pfrs - span.ohm span.glue nosupport.js \
	| pfrs - para.ohm para.glue nosupport.js \
	| pfrs - div.ohm div.glue nosupport.js \
	| pfrs - font.ohm font.glue nosupport.js \
	| pfrs - unhtml.ohm unhtml.glue nosupport.js >$i
    chmod a+x $i 
done

echo
echo '*** running result ***'
echo
./$target
