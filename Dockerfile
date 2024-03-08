# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN mkdir -p /rubixgoplatform && \
    apt-get update && \
    apt-get install -y screen && \
    pip install --no-cache-dir -r requirements.txt

# Make port 5050 available to the world outside this container
EXPOSE 5050

# Run bridge.py when the container launches
CMD ["python3", "bridge.py"]