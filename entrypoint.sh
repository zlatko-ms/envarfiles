#!/bin/sh -l

# just pass the command line to the python parser 
params=$(echo $@)
r=$(/usr/bin/python3 /processor.py $params)




