#!/bin/sh -l

varfile=$1
output="from $varfile : "

echo "myvalue=ZDBGValue" >> $GITHUB_ENV

if [ -z "$varfile" ] ; then
    echo "ERROR : missing varfile parameter"
else:
    while read p; do
        k=$(echo $p | sed s'/[ ]*=[ ]*/=/g')
        n=$(echo $k | cut -f1 -d'=')
        v=$(echo $k | cut -f2 -d'=')
        echo "$k" >> $GITHUB_ENV
        output="$output $k"
    done < "$varfile"
fi
echo "definitions=$output" >> $GITHUB_OUTPUT



