#!/bin/sh -l

paths=$1
output=""

function logMessage() {
    level = $1
    message = $2
    now = `date +%Y%m%d-%H%M%S`
    echo "[$now] [$level] $message"
}

function readVariablesFiles() {

    varfile = $1

    #output="$output $varfile=["

    while read p; do
        k=$(echo $p | sed s'/[ ]*=[ ]*/=/g')
        n=$(echo $k | cut -f1 -d'=')
        v=$(echo $k | cut -f2 -d'=')
        echo "[ZDBG] checking if $n exists"
        echo "[ZDBG] current value of $n is ${!$n}"
        echo "[ZDBG] file value of $n is $v"
        #output=" $output $k"
        echo "$k" >> $GITHUB_ENV
    done < "$varfile"

    #output="$output ]"

}


logMessage "INFO" "Starting processing"


# let's parse all the provided files
for varfile in $paths; do
    echo "[ZDBG] file = $varfile"

    if [ -f "$varfile" ] ; then 
        echo "[INFO] reading variable definitions from file $varfile"
        readVariablesFiles "$varfile"
    else
        echo "[WARN] ignoring file $varfile as it cannot be accessed"
    fi

done


#if [ "x$varfile" == "x" ] ; then
#    echo "ERROR : no input specified"
#    exit 255
#fi



# output="$varfile:["
# while read p; do
#     k=$(echo $p | sed s'/[ ]*=[ ]*/=/g')
#     n=$(echo $k | cut -f1 -d'=')
#     v=$(echo $k | cut -f2 -d'=')
#     output="$output $k"
#     echo "$k" >> $GITHUB_ENV
# done < "$varfile"
# output="$output]"
# echo "definitions=$output" >> $GITHUB_OUTPUT




