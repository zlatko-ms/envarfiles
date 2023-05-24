#!/bin/sh -l


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
                logMessage "info" "overriding $n='$v'"
                echo "$k" >> $GITHUB_ENV
            fi
        else
            logMessage "info" "defining $n='$v'"
            echo "$k" >> $GITHUB_ENV
        fi
    done < "$varfile"
}

function logMessage() {
    levelIn=$1
    message=$2
    if [ "$logs" == "TRUE" ] ; then 
        level=`echo "$levelIn" | tr '[:lower:]' '[:upper:]'`
        now=`date +%Y%m%d-%H%M%S`
        echo "[$now] varfiletoenv [$level] $message"
    fi
}

# some fun with parms
params=$(echo $@)
logs="FALSE"
override="FALSE"
outfile=$(mktemp -u)

logsFlag=$(echo "$params" | grep "logs=true" )
overrideFlag=$(echo "$params" | grep "override=true" )

if [ -n "$logsFlag" ] ; then 
    logs="TRUE"
fi

if [ -n "$overrideFlag" ] ; then 
    override="TRUE"
fi

# excute python parser and redirect the output to the temp file
$(/usr/bin/python3 ./processor.py $params outfile=$outfile)

# parse the output and declare vars
readVariablesFiles $override $outfile




