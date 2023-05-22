#!/bin/sh -l

override=`echo "$1" | tr '[:lower:]' '[:upper:]'`
logs=`echo "$2" | tr '[:lower:]' '[:upper:]'`
paths=$3
output="["


echo "ZDBG >>> logs=$logs"

function logMessage() {
    levelIn=$1
    message=$2
    if [ "$logs" == "TRUE" ] ; then 
        level=`echo "$levelIn" | tr '[:lower:]' '[:upper:]'`
        now=`date +%Y%m%d-%H%M%S`
        echo "[$now] [$level] [varfiletoenv] $message"
    fi
}

function readVariablesFiles() {

    overrideVar=$1
    varfile=$2
    
    while read p; do
        k=$(echo $p | sed s'/[ ]*=[ ]*/=/g')
        n=$(echo $k | cut -f1 -d'=')
        v=$(echo $k | cut -f2 -d'=')
        eval current="\$$n"
        if [ -n "$current" ]; then
            if [ "$overrideVar" == "TRUE" ]; then
                logMessage "info" "overriding $n='$v' from file $varfile"
                echo "$k" >> $GITHUB_ENV
            fi
        else
            logMessage "info" "defining $n='$v' from file $varfile"
            echo "$k" >> $GITHUB_ENV
        fi
    done < "$varfile"

}

for varfile in $paths; do
    if [ -f "$varfile" ] ; then 
        output="$output $varfile"
        readVariablesFiles "$override" "$varfile"
    else
        logMessage "warn" "ignoring file $varfile as it cannot be found"
    fi
done

echo "processed=$output ]" >> $GITHUB_OUTPUT





