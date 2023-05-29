#!/bin/bash

function usage {

    errorMessage=$1

    if [ "x" != "x$errorMessage" ]; then
        echo ""
        echo "ERROR  : $errorMessage"
        echo ""
    fi
    echo "USAGE  : rebase_workflow -d path/to/workflows -s sourceBranchName -t targetBranchName"
    echo "PARAMS :"
    echo "  -d : directory of the workflow files to rebase, defaults to .github/workflows"
    echo "  -s : sourceBranchName, for instance main"
    echo "  -t : targetBranchName, for instance 9-fix-my-bug"
    echo ""
    exit 255

}

while getopts 's:t:d:' OPTION; do
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

if [ -z "$directory" ] ; then 
  directory=".github/workflows"
fi

if [ -z "$source" ]; then usage "missing mandatory param -s" ; fi
if [ -z "$target" ]; then usage "missing mandatory param -t" ; fi

if [ -d "$directory" ] ; then
    for f in `find "$directory" -type f -name "*.yml"` ; do
      echo "[INFO] processing file $f"       
      perl -pi -e "s/envarfiles\@$source/envarfiles\@$target/g" $f
      # branches: [ "main" ]
      perl -pi -e "s/branches\: \[ \"$source\" \]/branches\: \[ \"$target\" \]/g" $f
    done
else
    echo "ERROR : unable to access directory $directory to peform rebase"
    exit 255
fi 

