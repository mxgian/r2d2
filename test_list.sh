#!/bin/bash
/home/pi/r2d2/dropbox_uploader.sh list   | awk '{ print $NF }' > /tmp/checklist

for i in $(cat /tmp/checklist);
do 
echo "deleting $i"
/home/pi/r2d2/dropbox_uploader.sh delete $i
done

