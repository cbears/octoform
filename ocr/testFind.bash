#!/bin/bash
cd 1001
firstRun=1
for i in *.png; do
  if [[ $i =~ "[0-9]{4}-[0-9]{3}.png" ]] ; then
    while [ `jobs -p | wc -l` -gt 5 ] ; do
      sleep 1
    done
    if [ $firstRun ] ; then 
      echo "Initializing system and processing $i"
      echo python -OO ../findBarcode.py $i 2>&1 > /dev/null &
      python -OO ../findBarcode.py $i 
      firstRun=
    else
      echo "Processing $i"
      python -OO ../findBarcode.py $i &
    fi
  fi
done;
