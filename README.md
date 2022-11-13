# TUIAlarm
A TUI to create an alarm that suspends your machine and wakes you with an audio file.


## Introduction
This application uses textual to create a TUI which sole purpose is to start a bash script with the correct attribute (duration of suspension).
To suspend the machine rtcwake is used.
It is totally possible to modify the executed scripts to one's own needs. The scripts in this repo shall mainly serve as examples.

This has been tested on Ubuntu 20.04.4 LTS

## Requirements
The only requirement at this point is textual==0.4.0  
It can be easily installed with pip.

## Usage
After cloning the repository, make sure to make the scripts executable.
Unfortunatly rtcwake needs root to work, therefore it is necessary to add rtcwake to the sudoers file. Please do this with caution,
since the file is essential and doing so, will allow anyone to execute rtcwake with root permissions.

To start the application simply use:

```
./alarm.py
```
