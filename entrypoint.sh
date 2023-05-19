#!/bin/sh -l

varfile=$1
output=""

if [ "x$varfile" == "x" ] ; then
    echo "ERROR : no input specified"
    exit 255
fi

output="$varfile:["
while read p; do
    k=$(echo $p | sed s'/[ ]*=[ ]*/=/g')
    n=$(echo $k | cut -f1 -d'=')
    v=$(echo $k | cut -f2 -d'=')
    output="$output $k"
    echo "$k" >> $GITHUB_ENV
done < "$varfile"
output="$output]"
echo "definitions=$output" >> $GITHUB_OUTPUT




