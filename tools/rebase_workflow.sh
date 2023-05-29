#!/bin/bash

function usage {

    errorMessage=$1

    if [ "x" != "x$errorMessage" ]; then
        echo ""
        echo "ERROR  : $errorMessage"
        echo ""
    fi
    echo "USAGE  : rebase_workflow -w path/to/workflow.yml -s sourceBranchName -t targetBranchName"
    echo "PARAMS :"
    echo "  -w : path to the worfklow file to rebase"
    echo "  -d : directory of the workflow files to rebase"
    echo "  -s : sourceBranchName, for instance main"
    echo "  -t : targetBranchName, for instance 9-fix-my-bug"
    echo ""
    exit 255

}

while getopts 'w:s:t:' OPTION; do
  case "$OPTION" in 
    w) 
      workflow="$OPTARG"
      ;;

    d) 
      directory="$OPTARG"
      ;;

    s)
      source="$OPTARG"
      ;;

    t)
      target="$OPTARG"
      ;;

    ?) 
      usage ""
      exit 1
      ;;
  esac
done

if [ -z "$workflow" or -z "$directory" ]; then usage "missing one of the mandatory params -w or -d " ; fi
if [ -z "$source" ]; then usage "missing mandatory param -s" ; fi
if [ -z "$target" ]; then usage "missing mandatory param -t" ; fi

echo "INFO : processing file $workflow"

if [ -f "$workflow" ] ; then 
    perl -pi -e "s/varfiletoenv\@$source/envarfiles\@$target/g" $workflow
    # branches: [ "main" ]
    perl -pi -e "s/branches\: \[ \"$source\" \]/branches\: \[ \"$target\" \]/g" $workflow
elif [ -d "$directory" ] ; then
    files=$(find "$directory" -type f -name "*.yml" )
    for f in files:
      perl -pi -e "s/varfiletoenv\@$source/envarfiles\@$target/g" $f
      # branches: [ "main" ]
      perl -pi -e "s/branches\: \[ \"$source\" \]/branches\: \[ \"$target\" \]/g" $f      
else
    echo "ERROR : unable to access file(s) to peform rebase"
    exit 255
fi 

