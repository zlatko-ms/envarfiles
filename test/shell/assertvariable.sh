#!/bin/bash

# asserts an env variable is defined and equals to the expected value
function assertDefinedAndEqualTo() {  
    name=$1
    expected=$2
    if [ -z "${!name}" ] ; then
        echo "[ERROR] variable $name is not defined";
        exit 255;
    fi
    if [ "${!name}" != "$expected" ] ; then 
        echo "[ERROR] variable $name , expected=$expected provided=${!name}";
        exit 255;
    fi
}