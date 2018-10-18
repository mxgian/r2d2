#!/bin/bash
#/home/pi/r2d2/dropbox_uploader.sh list   | awk '{ print $NF }' > /tmp/checklist
 /home/pi/r2d2/dropbox_uploader.sh list   | awk  '{ NF1=NF-1; print  $NF1 " " $NF }' > /tmp/checklist

 IFS=$'\r\n' GLOBIGNORE='*' command eval  'XYZ=($(cat /tmp/checklist))'
for i in "${XYZ[@]}"
do 
echo "deleting ${i}"
#/home/pi/r2d2/dropbox_uploader.sh delete $i
done
