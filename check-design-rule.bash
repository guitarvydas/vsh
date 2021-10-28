#!/bin/bash
cat - >_errors.txt
if grep -q 'FATAL' _errors.txt
then
    cat _errors.txt 1>&2
    echo 'quitting due to design rule failure' 1>&2
    exit 1
fi
rm _errors.txt
