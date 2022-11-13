#!/bin/bash
if [[ ! ("$#" == 1 && $1 =~ ^[0-9]+$) ]]; then 
    echo 'Invalid Argument(s)'
    exit 1
fi
sudo rtcwake -m mem -s $1 &>/dev/null
sleep 10 &>/dev/null
rhythmbox /home/nico/Music/Alarm.mpga &>/dev/null &
sleep 2
wmctrl -a TUIAlarm &>/dev/null
