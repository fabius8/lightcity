#!/bin/sh

cd tools/
./convertcity.py

cd ..

echo "Do you wish to run lightcity?" 

file=`ls tools/1*.json`

select yn in "Yes" "No"; do
    case $yn in
        Yes ) ./lightcity.py $file; break;;
        No ) exit;;
    esac
done

mv tools/1*.json .
