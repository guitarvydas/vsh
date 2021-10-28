#!/bin/bash
cat - >_errors.txt
if grep -q 'FATAL' _errors.txt
then
    cat _errors.txt
    echo quitting due to FATAL
    exit 1
fi
rm _errors.txt
