#!/bin/bash

# This script opens 4 terminal windows.

i="0"

while [ $i -lt 60 ]
do
        /home/pi/r2d2/monitor_ifttt.sh
        sleep 60
i=$[$i+1]
done