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

function assertNotDefined() {
    name=$1
    if [ -z "${!name}" ] ; then
        # do nothing
    else:
        echo "[ERROR] variable $name is defined while expected not to be";
        exit 255;
}