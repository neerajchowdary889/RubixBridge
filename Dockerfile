# Use an official Ubuntu runtime as a parent image
FROM ubuntu:20.04

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN mkdir -p /rubixgoplatform && \
    apt-get install -y screen && \
    apt-get install -y net-tools && \
    apt-get install -y lsof && \
    pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Make port 5050 available to the world outside this container
EXPOSE 5050
# Run bridge.py when the container launches
CMD ["python3", "bridge.py"]