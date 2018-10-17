#!/bin/bash

# This script opens 4 terminal windows.

declare -a arr=("scared" "no" "bipod" "angry" "confident" "tripod" "sad" "alarm" "laugh" "surprise" "chatty" "yes" "happy" "ionblast" "annoyed" "excited")

# robot needs to be r2d2 or q5. no error checking
robot = $1
for i in "${arr[@]}"
do 
 /home/pi/r2d2/r2d2.py robot -c $i
done
