#!/bin/sh

./countdown.py

for file in 1*.json
do
    echo $file
    #./lightcity.py $file
done

