#!/bin/bash

# Check your paths here
/home/pi/r2d2/dropbox_uploader.sh list  > /tmp/ifttt

File="/tmp/ifttt"
echo "checking for file"
# Monitor to turn L1 on - check your paths here
if grep -q r2d2.txt "$File"; then
   /home/pi/r2d2/dropbox_uploader.sh delete r2d2.txt && /bin/rm /tmp/ifttt && echo "Time: $(date) got email" >> /tmp/L1.log && /home/pi/r2d2/r2d2.py r2d2 -c happy
fi