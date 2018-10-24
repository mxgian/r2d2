#!/bin/bash

# XX Check your paths here
/home/pi/r2d2/dropbox_uploader.sh list  > /tmp/ifttt

File="/tmp/ifttt"

# do some checks, if we ran an alert in the last 5 mins, do not run the alert
lastrun="$(cat /tmp/checkstamp)"
rightnow="$(/bin/date +%s)"
echo "lastostamp ${lastrun} , ${rightnow}"
# Monitor to turn L1 on - check your paths here
if grep -q r2d2.txt "$File"; then
   /home/pi/r2d2/dropbox_uploader.sh delete r2d2.txt && /bin/rm /tmp/ifttt && echo "Time: $(date) got email" >> /tmp/L1.log && /home/pi/r2d2/r2d2.py r2d2 -c happy
fi

#clean
if grep -q r2-abh.txt "$File"; then
   /home/pi/r2d2/dropbox_uploader.sh delete r2-abh.txt && /bin/rm /tmp/ifttt && echo "Time: $(date) got email" >> /tmp/L1.log && /home/pi/r2d2/r2d2.py r2d2 -c laugh
fi

# this section cleans up the dir if there are files left over, for example if the monitor script crashes or mails come in too fast and we have multiple files (1,2,3), in this case dropbox adds n+1 file instead of creating the r2d2.txt and it won't trigger the script.  
# this code would need to be cleaned up to handle multiple use cases
 /home/pi/r2d2/dropbox_uploader.sh list   | awk  '{ NF1=NF-1; print  $NF1 " " $NF }' > /tmp/checklist

 IFS=$'\r\n' GLOBIGNORE='*' command eval  'XYZ=($(cat /tmp/checklist))'
for i in "${XYZ[@]}"
do 
echo "deleting ${i}"
/home/pi/r2d2/dropbox_uploader.sh delete "$i"
done

#/home/pi/r2d2/dropbox_uploader.sh list   | awk '{ print $NF }' | grep r2 > /tmp/checklist

#for i in $(cat /tmp/checklist);
#do 
#echo "deleting $i"
#/home/pi/r2d2/dropbox_uploader.sh delete $i
#done

/bin/rm /tmp/checklist
/bin/date +%s > /tmp/checkstamp