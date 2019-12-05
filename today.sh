#!/bin/sh

for file in 1*.json
do
    ./lightcity.py $file --freq 1
done
