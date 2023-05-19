varfile=$1
output="["

echo "myvalue=ZDBGValue" >> $GITHUB_ENV
echo "[ZDBG] processing file $varfile"

while read p; do
    k=$(echo $p | sed s'/[ ]*=[ ]*/=/g')
    n=$(echo $k | cut -f1 -d'=')
    v=$(echo $k | cut -f2 -d'=')
    echo "$k" >> $GITHUB_ENV
done < "$varfile"



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

#echo "definitions=none from varfile $varfile"