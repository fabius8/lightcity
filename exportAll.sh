#!/bin/bash

cityjsons=$(ls . | grep json)

for f in $cityjsons;
do ./convert2gpx.py $f;
done;

