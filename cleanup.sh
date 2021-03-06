#!/bin/bash
# this section cleans up the dir if there are files left over, for example if the monitor script crashes or mails come in too fast and we have multiple files (1,2,3), in this case dropbox adds n+1 file instead of creating the r2d2.txt and it won't trigger the script.  
# this code would need to be cleaned up to handle multiple use cases
 /home/pi/r2d2/dropbox_uploader.sh list   | awk  '{ NF1=NF-1; print  $NF1 " " $NF }' > /tmp/checklist

IFS=$'\r\n' GLOBIGNORE='*' command eval  'XYZ=($(cat /tmp/checklist))'
for i in "${XYZ[@]}"
do 
echo "deleting ${i}"
/home/pi/r2d2/dropbox_uploader.sh delete "$i"
done

/bin/rm /tmp/checklist 