#!/bin/sh

for file in 1*.json
do
    ./lightcity.py $file
done
