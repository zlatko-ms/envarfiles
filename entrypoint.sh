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
    logMessage "info" "reading variable definitions from $varfile"

    while read p; do
        k=$(echo $p | sed s'/[ ]*=[ ]*/=/g')
        n=$(echo $k | cut -f1 -d'=')
        v=$(echo $k | cut -f2 -d'=')
        logMessage "debug" "current var $n value is ${!n}"
    #     echo "[ZDBG] current value of $n is ${!$n}"
    #     echo "[ZDBG] file value of $n is $v"
    #     #output=" $output $k"
        echo "$k" >> $GITHUB_ENV
    done < "$varfile"

    #output="$output ]"

}


logMessage "INFO" "Starting variable definition processing"


# let's parse all the provided files
for varfile in $paths; do
    if [ -f "$varfile" ] ; then 
        readVariablesFiles "$varfile"
    else
        logMessage "warn" "ignoring file $varfile as it cannot be found"
    fi

done


#if [ "x$varfile" == "x" ] ; then
#    echo "ERROR : no input specified"
#    exit 255
#fi





