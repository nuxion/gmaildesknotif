#!/bin/bash
export DISPLAY=:0

message=$1
/usr/bin/notify-send -u critical $message 
touch test.txt
