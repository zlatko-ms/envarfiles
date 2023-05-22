#!/bin/sh -l

paths=$1
output=""

echo "[ZDBG] paths=$paths"

# let's parse all the provided files
for varfile in $paths; do
    echo "[ZDBG] file = $varfile"

    if [ -f "$varfile"]; then 
        echo "[ZDBG] reading file $varfile"
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




