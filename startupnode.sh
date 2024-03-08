#!/bin/bash
logfile="/home/ubuntu/cronlog/rubixstartup.log"
#screen -dmS node2 -L -Logfile $log_file $runfile
echo "Starting session" >> $logfile
screen -dmS node1 /home/ubuntu/rubix/rubixgoplatform/linux/rubixgoplatform run -p node1 -n 0 -s -port 20000 -testNet -grpcPort 10500
echo "Started session" >> $logfile
