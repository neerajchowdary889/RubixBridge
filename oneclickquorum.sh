#!/bin/bash
logfile="/home/ubuntu/cronlog/rubixstartup.log"
echo "Starting sessions" >> $logfile

base_port=20000
base_grpc_port=10500

#Primary Node in Port 20000/10500
screen -dmS "node0" rubixgoplatform run -p "node0" -n "$i" -s -port 20000 -testNet -grpcPort 10500

#Validator Nodes
for ((i=1; i<=6; i++)); do
  port=$((base_port + i - 1))
  grpc_port=$((base_grpc_port + i - 1))
  screen -dmS "node$i" rubixgoplatform run -p "node$i" -n "$i" -s -port "$port" -testNet -grpcPort "$grpc_port"
  echo "Started session for node$i, port: $port, grpcPort: $grpc_port" >> $logfile
done

echo "All sessions started" >> $logfile
