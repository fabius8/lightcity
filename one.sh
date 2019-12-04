#!/bin/sh

cd tools/
./convertcity.py

cd ..

for file in tools/1*.json
do
    lightcity.py $file
done

mv tools/1*.json .
