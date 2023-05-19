#!/bin/sh -l

varfile=$1
output="["

echo "definitions=none from varfile $varfile"

# if [ -z "$varfile" ] ; then
#     echo "ERROR : missing varfile parameter"
# else:
#     while read p; do
#             k=$(echo $p | sed s'/[ ]*=[ ]*/=/g')
#             n=$(echo $k | cut -f1 -d'=')
#             v=$(echo $k | cut -f2 -d'=')
#             output="$output $n=$v"
#             echo "$k" >> $GITHUB_ENV
#             echo "ZDBG adding definition $k"

#     done < $varfile
#     echo "definitions=$output" >> $GITHUB_OUTPUT
# fi


