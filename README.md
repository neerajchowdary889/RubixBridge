# Setting Up rubixgoplatform and Running the Quorum

## To run in Local PC (Non-docker setup)
1. **Setting up .env**
   - Navigate to .env.example and provide the required absolute paths for rubixgoplatform. Ensure to follow the path format shown in the examples within .env.example. 
   - Give required mongodb host address and port number.
   - make .env.example into .env file by removing .example suffix.

2. **Get to go**
   - You are all set. Now, you don't need to make changes anywhere in the codebase. You can manage everything just by editing the .env file.

## To run as docker network
1. **Prerequisite: Set up the `rubixgoplatform` codebase for Docker**
   - I need to manage Git permissions before uploading it to GitHub.
   - Documentation for this process will be provided shortly.

2. **Open docker-compose.yaml file**
   - go to rubixgoplatform container section in the file
   ```  
   rubixgoplatform:
    build:
      context: /home/neeraj-xps/Codes/rubixgoplatform
      dockerfile: Dockerfile.multistage
    user: root
    volumes:
      - shared_volume:/linux1
    ports:
      - "20000:20000"
      - "20001:20001"
      - "20002:20002"
      - "20003:20003"
      - "20004:20004"
      - "20005:20005"
      - "20006:20006"
      - "20007:20007"
      - "20008:20008"
      - "20009:20009"
    networks:
      - testnet
    depends_on:
      - "mongodb"
   ```

   - edit context path to your rubixgoplatform codebase's path. 

   - make sure all the listed ports are not occupied. To check use this command (it won't work in windows)
   ```./checkservice.sh 20000 20001 20002 20003 20004 20005 20006 20007 20008 20009```

   - to force-quit all the running services on that port using this command (it won't work in windows)
   ```./stopservice.sh 20000 20001 20002 20003 20004 20005 20006 20007 20008 20009```

3. **Build up Docker Network using docker-compose**
   - Open terminal and run this command to build the Docker Network.
   ``` docker-compose build rubixbridge_flask ```

   - Open another terminal and run this command to run the Docket Network.
   ``` docker-compose -f docker-compose.yaml up ```


# Running oneclickquorum.sh Script

## Prerequisites

Before running the "oneclickquorum.sh" script, make sure you have the following prerequisites in place:

- **Operating System**: These instructions are provided for Windows, macOS, and Linux.
- **`rubixgoplatform` Installation**: Ensure you have `rubixgoplatform` installed on your system.
- **Directory Path**: Navigate to the directory where the "oneclickquorum.sh" script is located.
- Make necessart changes to the path in the oneclickquorum file.

## Windows

1. **Open Command Prompt**:
   - Press `Win + R`, type `cmd`, and press Enter to open the Command Prompt.

2. **Navigate to the Script Directory**:
   - Use the `cd` command to navigate to the directory where the "oneclickquorum.sh" script is located.

3. **Run the Script**:
   - To run the script, use the following command:
     ```bash
     bash oneclickquorumwindows.bat
     ```

## macOS (formerly OS X)

1. **Open Terminal**:
   - Open the Terminal application.

2. **Navigate to the Script Directory**:
   - Use the `cd` command to navigate to the directory where the "oneclickquorum.sh" script is located.

3. **Run the Script**:
   - To run the script, use the following command:
     ```bash
     bash oneclickquorummac.sh
     ```

## Linux

1. **Open Terminal**:
   - Open a terminal.

2. **Navigate to the Script Directory**:
   - Use the `cd` command to navigate to the directory where the "oneclickquorum.sh" script is located.

3. **Make the Script Executable (if not already)**:
   - If the script is not already executable, you can make it executable by running:
     ```bash
     chmod +x oneclickquorum.sh
     ```

4. **Run the Script**:
   - To run the script, use the following command:
     ```bash
     ./oneclickquorum.sh
     ```

These steps will execute the "oneclickquorum.sh" script on Windows, macOS, and Linux, provided that you have set up `rubixgoplatform` and configured the script correctly for your environment.

They python script - bridge.py has an APIs to get details of the quorums and create quorumList.json file
Setting us the quorum and connecting them is manual for now. For instructions refer - https://docs.google.com/document/d/1GA8J9YALiRsNXq8XALS0Xi-jJeQtX-eyWQywem3-eno/edit

TODOs
- Need to write a script to setup and connect all the quorums.
