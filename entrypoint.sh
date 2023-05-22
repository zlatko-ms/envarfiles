#!/bin/sh -l

override=`echo "$1" | tr '[:lower:]' '[:upper:]'`
paths=$2
output="["


function logMessage() {
    levelIn=$1
    message=$2
    level=`echo "$levelIn" | tr '[:lower:]' '[:upper:]'`
    now=`date +%Y%m%d-%H%M%S`
    echo "[$now] [$level] $message"
}

function readVariablesFiles() {

    overrideVar=$1
    varfile=$2
    
    logMessage "info" "reading variable definitions from $varfile"
    
    while read p; do
        k=$(echo $p | sed s'/[ ]*=[ ]*/=/g')
        n=$(echo $k | cut -f1 -d'=')
        v=$(echo $k | cut -f2 -d'=')
        eval current="\$$n"
        
        logMessage "debug" "current var $n value is $current"

        if [ -n "$current" ]; then
            if [ "$overrideVar" == "TRUE" ]; then
                logMessage "debug" "overriding variable $n from file"
                echo "$k" >> $GITHUB_ENV
            fi
        else
            logMessage "debug" "defining variable $n from file"
            echo "$k" >> $GITHUB_ENV
        fi

        logMessage "info" "found variable definition $k"
        
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

# if [ "x$paths" == "x" ] ; then
#     logMessage "fatal" "no input files specified !"
#     exit 255
# fi





