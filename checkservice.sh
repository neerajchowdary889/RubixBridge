#!/bin/bash

# Loop over all arguments
for port in "$@"
do
    echo "Checking services on port $port"

    # Find the PID of the service running on the port
    pid=$(lsof -t -i:$port)
    echo "PID: $pid"

    if [ -n "$pid" ]; then
        echo "Service running on port $port --> PID: $pid"
    else
        echo "No service running on port $port"
    fi
done