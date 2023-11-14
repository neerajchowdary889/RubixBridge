#!/bin/bash
logfile="/home/ubuntu/cronlog/rubixstartup.log"
#screen -dmS node2 -L -Logfile $log_file $runfile
echo "Starting session" >> $logfile
screen -dmS node1 /home/ubuntu/rubix/rubixgoplatform/linux/rubixgop>
echo "Started session" >> $logfile
