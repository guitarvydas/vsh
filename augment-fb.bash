#!/bin/bash
tempname=_temp-$RANDOM
temp2name=_temp-$RANDOM
sort - >${tempname}
cat fb.pl ${tempname} >${temp2name}
mv ${temp2name} fb.pl
rm ${tempname}
