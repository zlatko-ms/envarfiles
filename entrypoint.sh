#!/bin/sh -l

paths=$1
output=""

function logMessage() {

    levelIn=$1
    message=$2
    level=`echo "$levelIn" | tr '[:lower:]' '[:upper:]'`
    now=`date +%Y%m%d-%H%M%S`
    echo "[$now] [$level] $message"

}

function readVariablesFiles() {

    varfile=$1
    outputRet="$varfile=["

    logMessage "info" "reading variable definitions from $varfile"

    while read p; do
        k=$(echo $p | sed s'/[ ]*=[ ]*/=/g')
        n=$(echo $k | cut -f1 -d'=')
        v=$(echo $k | cut -f2 -d'=')
        eval current="\$$n"
        #logMessage "debug" "current var $n value is $current"
        outputRet="$outputRet $k"
        echo "$k" >> $GITHUB_ENV
    done < "$varfile"
    outputRet="$outputRet ]"
    echo "$outputRet"
}


for varfile in $paths; do
    if [ -f "$varfile" ] ; then 
        retCall=$(readVariablesFiles "$varfile")
        output="$output $retCall"
    else
        logMessage "warn" "ignoring file $varfile as it cannot be found"
    fi

done

echo "definitions=$output" >> $GITHUB_OUTPUT

#if [ "x$varfile" == "x" ] ; then
#    echo "ERROR : no input specified"
#    exit 255
#fi





