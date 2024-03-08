#!/usr/bin/python3
import subprocess
from flask import Flask, request, jsonify, Response, send_file , render_template, redirect, session, url_for, send_from_directory
import requests,json, time, geocoder, sys
from flask_cors import CORS
from pymongo import MongoClient
import json
import os
# import ipfshttpclient
import ipfsapi
from dotenv import load_dotenv
from Run_commands import get_only_cid, upload_to_ipfs, download_from_ipfs

load_dotenv()

current_directory = os.getcwd()
print("Current Directory:", current_directory)

if os.path.isdir(os.getenv('env_WORK_DIR')):
    print("Changing to working directory:", os.getenv('env_WORK_DIR'))
    os.chdir(os.getenv('env_WORK_DIR'))
else:
    print("Working directory not found. Changing to current directory")
    os.chdir(current_directory)

# Define MongoDB connection information
MONGO_HOST = os.getenv('env_MONGO_URL')
MONGO_PORT = int(os.getenv('env_MONGO_PORT'))
MONGO_DB = os.getenv('env_MONGO_DB')

app = Flask(__name__)
CORS(app)

def security(fname):
	APILog={'timestamp':int(time.time()),
		'location': str(geocoder.ip(str(request.environ['REMOTE_ADDR'])).city),
		'clientAgent':str(request.headers.get('User-Agent')),
		'clientIP':str(request.environ['REMOTE_ADDR']),
		'API':fname}
	mongo_client = MongoClient(MONGO_HOST)
	db = mongo_client[MONGO_DB]
	MONGO_COLLECTION = "RubixBridgeAPILOG"
	collection = db[MONGO_COLLECTION]
	collection.insert_one(APILog)
	# mongo_client.close()

#CreateDID Parent API
@app.route('/api/createparentdid', methods=['GET'])
def createParentDID():
    security(str(sys._getframe().f_code.co_name))
    print("create ParentDID API")
    mongo_client = MongoClient(MONGO_HOST)
    db = mongo_client[MONGO_DB]
    MONGO_COLLECTION = "parentdid"
    collection = db[MONGO_COLLECTION]
    start_time = time.time()

    # Get the user input for the field (e.g., "AM" or "ISK")
    user_input = request.args.get('app', '')

    # Define a dictionary to map field values to ports
    field_to_port = {
		'AM': 20000,
		'ISK': 20001,
		'V1': 20002,
		'V2': 20003,
		'V3': 20004,
		'V4': 20005,
		'V5': 20006,
	}
        # Add more field-to-port mappings as needed
		

    # Default port (if the user input is not recognized)
    default_port = 2

    # Get the port based on user input; use the default if not found in the dictionary
    port = field_to_port.get(user_input, default_port)
    # Check if the user input is not recognized
    if port == default_port:
        error_message = f"Invalid Application: {user_input}."
        return jsonify({'error': error_message}), 400  # Return a JSON error response with a 400 status code
    
    # Define the API endpoint URL
    url = f'http://localhost:{port}/api/createdid'
    
    # Create a dictionary for form data
    form_data = {'did_config': (None, '{"type":0,"dir":"","config":"","master_did":"","secret":"My DID Secret","priv_pwd":"mypassword","quorum_pwd":"mypassword"}'),}

    # Specify the file to upload
    files = {'img_file': ('image.png', open(r'image.png', 'rb'), 'image/png')}

# Send a POST request with multipart/form-data
    try:
        response = requests.post(url, data=form_data, files=files)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(elapsed_time)
    # Check the response status code
        if response.status_code == 200:
             message = json.loads(response.text)
             if message['status'] == True:
                did = message['result']['did']
                peerid = message['result']['peer_id']
                print(str(request.environ['REMOTE_ADDR']))
                didpeerid={'status':True,
                           'createTime':end_time,
                           'port':port,
                           'did':did,
                           'peerid':peerid,
                           'timeTaken':elapsed_time,
                           'creatorIP':str(request.environ['REMOTE_ADDR']),
                           'location': str(geocoder.ip(str(request.environ['REMOTE_ADDR'])).city),
                           'clientAgent':str(request.headers.get('User-Agent')),
                           }
                print(didpeerid)
                momgodid=didpeerid
                collection.insert_one(momgodid)
                mongo_client.close()
                # Remove the _id field if it exists
                if '_id' in didpeerid:
                    didpeerid.pop('_id')
                return jsonify(didpeerid)
             else:
                print(message)
                return message

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        return (str(e))
    
#CreateDID Child API
@app.route('/api/createchilddid', methods=['GET'])
def createchildDID():
    security(str(sys._getframe().f_code.co_name))
    print("create childDID API")
    mongo_client = MongoClient(MONGO_HOST)
    db = mongo_client[MONGO_DB]
    MONGO_COLLECTION = "childdid"
    collection = db[MONGO_COLLECTION]

    # Get the user input for the field (e.g., "AM" or "ISK")
    user_input = request.args.get('app', '')
    did_input = request.args.get('did', '')

    # Define a dictionary to map field values to ports
    # Define a dictionary to map field values to ports
    field_to_port = {
        'AM': 20000,
        'ISK': 20001,
        'V1': 20002,
        'V2': 20003,
        'V3': 20004,
        'V4': 20005,
        'V5': 20006,
        
    }
    #Default port (if the user input is not recognized)
    default_port = 2
    # Get the port based on user input; use the default if not found in the dictionary
    port = field_to_port.get(user_input, default_port)
    # Check if the user input is not recognized
    if port == default_port:
        error_message = f"Invalid Application: {user_input}."
        return jsonify({'error': error_message}), 400  # Return a JSON error response with a 400 status code
    
    # Define the API endpoint URL
    alldidurl = f'http://localhost:{port}/api/getalldid'

    
    
    alldid = requests.get(alldidurl)
    alldid = json.loads(alldid.text)
    if did_input:
        parentDID = did_input
    else:
        parentDID = alldid['account_info'][0]['did']
    print(parentDID)
    start_time = time.time()
    # Define the API endpoint URL
    url = f'http://localhost:{port}/api/createdid'

    # Create a dictionary for form data
    formstring = '{"type":3,"dir":"","config":"","master_did":"","secret":"My DID Secret","priv_pwd":"mypassword","quorum_pwd":"mypassword"}'
    formstring = json.loads(formstring)
    formstring['master_did'] = parentDID
    formstring = json.dumps(formstring)
    form_data = {'did_config': (None, formstring)}

    # Specify the file to upload
    files = {'img_file': ('image.png', open(r'image.png', 'rb'), 'image/png')}

# Send a POST request with multipart/form-data
    try:
        response = requests.post(url, data=form_data, files=files)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(elapsed_time)
    # Check the response status code
        if response.status_code == 200:
        # Request was successful
            message = json.loads(response.text)
            if message['status'] == True:
                print(message['result']['did'])
                print(message['result']['peer_id'])
                didpeerid={'status':True,
                           'parentdid': parentDID,
                           'did':message['result']['did'],
                           'peerid':message['result']['peer_id'],
                           'timeTaken':elapsed_time,
                           'creatorIP':str(request.environ['REMOTE_ADDR']),
                           'location': str(geocoder.ip(str(request.environ['REMOTE_ADDR'])).city),
                           'clientAgent':str(request.headers.get('User-Agent')),}
                collection.insert_one(didpeerid)
                mongo_client.close()
                # Remove the _id field if it exists
                if '_id' in didpeerid:
                    didpeerid.pop('_id')
                return jsonify(didpeerid)
            else:
                print(message)
                return message
        else:
            print(f"POST request failed with status code {response.status_code}")
            print("Response content:", response.text)
            return response.text

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        end_time = time.time()
        elapsed_time = end_time - start_time
        return (str(e))
    
#Get all DIDs
@app.route('/api/getalldid', methods=['GET'])
def getalldid():
    security(str(sys._getframe().f_code.co_name))
    print("GetallDID API")

    # Get the user input for the field (e.g., "AM" or "ISK")
    user_input = request.args.get('app', '')

    field_to_port = {
        'AM': 20000,
        'ISK': 20001,
        'V1': 20002,
        'V2': 20003,
        'V3': 20004,
        'V4': 20005,
        'V5': 20006,
        # Add more field-to-port mappings as needed
    }


    default_port = 2

    # Get the port based on user input; use the default if not found in the dictionary
    port = field_to_port.get(user_input, default_port)
    # Check if the user input is not recognized
    if port == default_port:
        error_message = f"Invalid Application: {user_input}."
        return jsonify({'error': error_message}), 400  # Return a JSON error response with a 400 status code
    
    # Define the API endpoint URL
    alldidurl = f'http://localhost:{port}/api/getalldid'

    try:
        response = requests.get(alldidurl)

    # Check the response status code
        if response.status_code == 200:
        # Request was successful
            return json.loads(response.text)
        else:
            return json.loads(response.text)

    except requests.exceptions.RequestException as e:
        return (str(e))

@app.route('/api/savedatatoken', methods=['POST'])
def save_json():
    security(str(sys._getframe().f_code.co_name))
    print("saveDT")
    try:
        # Get JSON data from the API request
        user_data = request.json
        print(user_data)
        
        # Check if the JSON data is empty or malformed
        if not user_data:
            return jsonify({'error': 'Invalid JSON data.'}), 400

        # Save the JSON data to a file
        with open('datatoken.json', 'w') as file:
            json.dump(user_data, file)
        
        return jsonify({'message': 'JSON data saved successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/createdt', methods=['GET'])
def createdt():
    security(str(sys._getframe().f_code.co_name))
    print("createDT")
    start_time = time.time()

    # Get the user input for the field (e.g., "AM" or "ISK")
    user_input = request.args.get('app', '')

    # # Define a dictionary to map field values to ports
    # # Define a dictionary to map field values to ports
    field_to_port = {
        'AM': 20000,
        'ISK': 20001,
        'V1': 20002,
        'V2': 20003,
        'V3': 20004,
        'V4': 20005,
        'V5': 20006,
    #     # Add more field-to-port mappings as needed
    }

    # # Default port (if the user input is not recognized)
    
    default_port = 2

    # # Get the port based on user input; use the default if not found in the dictionary
    port = field_to_port.get(user_input, default_port)
    # # Check if the user input is not recognized
    if port == default_port:
        error_message = f"Invalid Application: {user_input}."
        return jsonify({'error': error_message}), 400  # Return a JSON error response with a 400 status code
    
    #To get parentDID
    alldidurl = f'http://localhost:{port}/api/getalldid'

    
    
    alldid = requests.get(alldidurl)
    alldid = json.loads(alldid.text)
    parentDID = alldid['account_info'][0]['did']
    print(parentDID)
       
    # Define the API endpoint URL
    url = f'http://localhost:{port}/api/create-data-token?did={parentDID}'

    formstring = '{"UserID": "1","UserInfo": "abc","CommitterDID": "cdid","BacthID": "10","FileInfo": "{}"}'
    formstring = json.loads(formstring)
    formstring['CommitterDID'] = parentDID
    # formstring = json.dumps(formstring)


    # url = 'http://localhost:20000/api/create-data-token?did=bafybmigqedkcsr3drksfhc5iwza7ajavdaaswsn3ro2cvlu6fgbypbqz7q'
    # form_data = {'UserID': '1','UserInfo': 'abc','CommitterDID': '{did}','BacthID': '10','FileInfo': '{}'}
    
    files = {'FileContent': ('datatoken.json', open('datatoken.json', 'rb'), 'application/json')}

    try:
        response = requests.post(url, data=formstring, files=files)
        print(response.text)
        
        #signature
        id=json.loads(response.text)
        id=id['result']['id']
        print(id)
        signdata={"id":str(id),"mode":0,"password":"mypassword"}
        signurl=f'http://localhost:{port}/api/signature-response'
        print(signurl)
        try:
            #calling signature API
            signresponse = requests.post(signurl, data=json.dumps(signdata))
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(elapsed_time)
            print(signresponse.text)
            return jsonify(json.loads(signresponse.text))
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            elapsed_time = end_time - start_time
            return (str(e))
    except requests.exceptions.RequestException as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        return (str(e))

@app.route('/api/commitdt', methods=['GET'])
def commitdt():
    security(str(sys._getframe().f_code.co_name))
    print('commitDT')
    start_time = time.time()

    # Get the user input for the field (e.g., "AM" or "ISK")
    user_input = request.args.get('app', '')

    field_to_port = {
        'AM': 20000,
        'ISK': 20001,
        'V1': 20002,
        'V2': 20003,
        'V3': 20004,
        'V4': 20005,
        'V5': 20006,
    }

    
    default_port = 2

    # # Get the port based on user input; use the default if not found in the dictionary
    port = field_to_port.get(user_input, default_port)
    # # Check if the user input is not recognized
    if port == default_port:
        error_message = f"Invalid Application: {user_input}."
        return jsonify({'error': error_message}), 400  # Return a JSON error response with a 400 status code
    
    #To get parentDID
    alldidurl = f'http://localhost:{port}/api/getalldid'
  
    alldid = requests.get(alldidurl)
    alldid = json.loads(alldid.text)
    parentDID = alldid['account_info'][0]['did']
    print(parentDID)
    checkdturl = f'http://localhost:{port}/api/get-data-token?did={parentDID}'
    
    try:
        checkdturlresponse = requests.get(checkdturl)
        print(checkdturlresponse.text)
        
        commitdturl = f'http://localhost:{port}/api/commit-data-token?did={parentDID}&batchID={parentDID}'
        
        response = requests.post(commitdturl)
        print(response)
        print(response.text)
        if response.status_code == 200:
            response_data = response.json()
            if 'status' in response_data and response_data['status'] is False:
            # Return the response
                return jsonify(response.text)
            
            else:
            
                #signature
                id=json.loads(response.text)
                id=id['result']['id']
                print(id)
                signdata={"id":str(id),"mode":0,"password":"mypassword"}
                signurl=f'http://localhost:{port}/api/signature-response'
                print(signurl)@app.route('/api/getfromipfs', methods=['POST','GET'])

                try:
                    #calling signature API
                    signresponse = requests.post(signurl, data=json.dumps(signdata))
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    print(elapsed_time)
                    print(signresponse.text)
                    return jsonify(json.loads(signresponse.text))
                except requests.exceptions.RequestException as e:
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    return (str(e))
        else:
            return jsonify(response.text)

    
    
    except requests.exceptions.RequestException as e:
        end_time = time.time()
        elapsed_time = end_time - start_time
        return (str(e))  

@app.route('/api/shutdownall')
def shutdownall():
    security(str(sys._getframe().f_code.co_name))
    node_statuses = {}

    node_to_port = {
        'AM': 20000,
        'ISK': 20001,
        'V1': 20002,
        'V2': 20003,
        'V3': 20004,
        'V4': 20005,
        'V5': 20006,
    }

    for node_name, port in node_to_port.items():
        url = f'http://localhost:{port}/api/shutdown'
        
        try:
            response = requests.get(url)
            print(port, response.status_code)
            if response.status_code == 200:
                node_statuses[node_name] = "Shutdown complete"
            else:
                node_statuses[node_name] = "Unable to connect (Node may be down)"
        except requests.exceptions.RequestException as e:
            node_statuses[node_name] = f"Unable to connect (Error: {str(e)})"

    return jsonify(node_statuses)

@app.route('/api/testallnodes', methods=['GET'])
def testAllNodes():
    security(str(sys._getframe().f_code.co_name))
    node_statuses = {}

    node_to_port = {
        'AM': 20000,
        'ISK': 20001,
        'V1': 20002,
        'V2': 20003,
        'V3': 20004,
        'V4': 20005,
        'V5': 20006,
    }

    for node_name, port in node_to_port.items():
        url = f'http://localhost:{port}/api/getalldid'
        
        try:
            response = requests.get(url)
            # print(port, response.status_code)
            if response.status_code == 200:
                node_statuses[node_name] = "Node is fine"
            else:
                node_statuses[node_name] = "Unable to connect (Node may be down)"
        except requests.exceptions.RequestException as e:
            node_statuses[node_name] = f"Unable to connect (Error: {str(e)})"

    return jsonify(node_statuses)

@app.route('/api/createquorum', methods=['GET'])
def createquorum():
    security(str(sys._getframe().f_code.co_name))
    user_input = request.args.get('app', '')
    field_to_port = {
        'AM': 20000,
        'ISK': 20001,
        'V1': 20002,
        'V2': 20003,
        'V3': 20004,
        'V4': 20005,
        'V5': 20006,
    }

    default_port = 2

    # Get the port based on user input; use the default if not found in the dictionary
    port = field_to_port.get(user_input, default_port)
    # Connect to MongoDB (assuming it's running on localhost, default port)
    client = MongoClient(MONGO_HOST)

    # Select the MongoDB database and collection where your records are stored
    db = client[MONGO_DB]
    collection = db['quorumdetails']

    # Query the database to retrieve the 7 records
    records = collection.find({'port': {'$ne': int(port)}}).limit(6)

# Create a list to store the quorumlist
    quorumlist = []

# Iterate through the retrieved records and format them
    for record in records:
        did = record.get('did', '')
        peerid = record.get('peerid', '')
        if did and peerid:
            quorum_entry = {
                'type': 2,
                'address': f"{peerid}.{did}"
            }
            quorumlist.append(quorum_entry)

# Close the MongoDB connection
    client.close()

# Save the quorumlist to a JSON file
    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # '' = os.path.join(current_directory, 'quorumlist.json')
    with open('quorumlist.json', 'w') as json_file:
        json.dump(quorumlist, json_file, indent=4)
    # print(json_file_path)
    return quorumlist

@app.route("/api/getallquorum", methods=['GET'])
def getallquorum():
    security(str(sys._getframe().f_code.co_name))
    user_input = request.args.get('app', '')
    field_to_port = {
        'AM': 20000,
        'ISK': 20001,
        'V1': 20002,
        'V2': 20003,
        'V3': 20004,
        'V4': 20005,
        'V5': 20006,
    }
    default_port = 2

    # Get the port based on user input; use the default if not found in the dictionary
    port = field_to_port.get(user_input, default_port)
    # Check if the user input is not recognized
    if port == default_port:
        error_message = f"Invalid Application: {user_input}."
        return jsonify({'error': error_message}), 400  # Return a JSON error response with a 400 status code
    
    # Define the API endpoint URL
    alldidurl = f'http://localhost:{port}/api/getallquorum'

    try:
        response = requests.get(alldidurl)

    # Check the response status code
        if response.status_code == 200:
        # Request was successful
            return json.loads(response.text)
        else:
            return json.loads(response.text)

    except requests.exceptions.RequestException as e:
        return (str(e))


@app.route("/api/getalldt",methods=["GET"])
def getalldt():
	print('getalldt')
	security(str(sys._getframe().f_code.co_name))
	user_input = request.args.get('app', '')
	field_to_port = {
		'AM': 20000,
		'ISK': 20001,
		'V1': 20002,
		'V2': 20003,
		'V3': 20004,
		'V4': 20005,
		'V5': 20006,
	}
	default_port = 2
	port = field_to_port.get(user_input, default_port)
	if port == default_port:
		error_message = f"Invalid Application: {user_input}."
		return jsonify({'error': error_message}), 400  # Return a JSON error response with a 400 status code

	alldidurl = f'http://localhost:{port}/api/getalldid'
	alldid = requests.get(alldidurl)
	alldid = json.loads(alldid.text)
	parentDID = alldid['account_info'][0]['did']
	print(parentDID)

	url = f'http://localhost:{port}/api/get-data-token?did={parentDID}'
	headers = {'accept': 'application/json'}

	try:
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			json_response = response.json()
			print("Response JSON:", json_response)
			return jsonify(json_response)
		else:
			print("Request failed with status code:", response.status_code)
			return response.status_code
	except requests.exceptions.RequestException as e:
		print("Request error:", e)
		return jsonify("Request error:", e)


@app.route("/api/fetchdt", methods=['GET'])
def fetchdt():
    print("fetchdt")
    security(str(sys._getframe().f_code.co_name))
    user_input = request.args.get('txid', '')
    print(user_input)
    # try:
    client = ipfsapi.connect('localhost', 4002)
    		# Fetch data from IPFS using the token ID
    data = client.cat(user_input)

    		# Assuming it's a text file, decode the bytes to a string
    decoded_data = data.decode('utf-8')

    		# Print the fetched data
    print(decoded_data)
    client.close()
    return (str(decoded_data))

@app.route("/api/fetchall", methods=['GET'])
def fetch_all():
    security(str(sys._getframe().f_code.co_name))
    print("fetch_all")
    start_time = time.time()

    # Define a dictionary to map field values to ports
    field_to_port = {
        'AM': 20000,
        'ISK':20001,
        'V1': 20002,
        'V2': 20003,
        'V3': 20004,
        'V4': 20005,
        'V5': 20006,
    }

    # Default port (if the user input is not recognized)
    default_port = 2

    if os.path.exists('responses.json'):
        with open("responses.json", "w") as file:
        # Use the `truncate()` method to clear the file's content
            file.truncate()
        responses = []
    else:
        responses = []


    for user_input in ['AM', 'ISK', 'V1', 'V2', 'V3', 'V4', 'V5']:
        # Get the port based on user input; use the default if not found in the dictionary
        port = field_to_port.get(user_input, default_port)

        # Check if the user input is not recognized
        if port == default_port:
            error_message = f"Invalid Application: {user_input}."
            return jsonify({'error': error_message}), 400  # Return a JSON error response with a 400 status code

        # To get parentDID
        parentdidurl = f'http://localhost:5050/api/createparentdid?app={user_input}'
        print(parentdidurl) #http://localhost:5050/api/createparentdid?app=AM

        alldid = requests.get(parentdidurl)
        print(alldid.text)
        alldid = json.loads(alldid.text)
        parentDID = alldid['did']
        print(parentDID)

        # Add the user_input and default_port to the response
        response = {
            'did': parentDID,
            'user_input': user_input,
            'port': port
        }

        # Add the response to the list
        responses.append(response)

    # Save the responses to a JSON file
    with open('responses.json', 'w') as file:
        json.dump(responses, file)

    return jsonify({'message': 'Data fetched and saved successfully.'}), 200

def getFilepath(path) -> (bool,str,str):
    try:
        directory = os.path.dirname(path).split("Saving file(s) to")[-1].strip()
        filename = os.path.basename(path) 
        return(True,directory,filename)
    except:
        return(False,None,None)
    
@app.route('/api/getfromipfs', methods=['POST','GET'])
def get_from_ipfs():
    if request.method == 'POST':
        CID = request.form['CID']
        print(CID)
        File = download_from_ipfs(
            CID=CID
            )
        print(File)
        status, directory, _filename = getFilepath(File)

        if status:
            try:
                return {"message": "File Downloaded succesfully"}, 200
            except Exception as e:
                print(e)
                return {"message": "File not found"}, 404
        else:
            return {"message": "File not found"}, 404
    else:
        return render_template('upload.html')

@app.route('/test/add', methods=['POST'])
def add_to_mongo():
    data = request.get_json()

    try:
        mongo_client = MongoClient(MONGO_HOST)
        db = mongo_client[MONGO_DB]
        MONGO_COLLECTION = "test"
        collection = db[MONGO_COLLECTION]

        momgodid=data
        collection.insert_one(momgodid)
        mongo_client.close()

        return jsonify({'message': 'Data inserted successfully.'}), 200
    except Exception as e:
        return jsonify({'message': 'Data not inserted.', 'error': str(e)}), 500

@app.route('/api/turnonnodes')
def turn_on_nodes():
    try:
        subprocess.call(["./oneclickquorum.sh"])

        return jsonify({'message': 'Shell script executed successfully.'}), 200
    
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Failed to execute shell script.', 'error': str(e)}), 500

@app.route('/api/forcestopnodes')
def force_stop_nodes():
    try:
        # Define the ports you want to stop services on
        ports = [20000, 20001, 20002, 20003, 20004, 20005, 20006]

        # Convert the ports to strings
        ports = [str(port) for port in ports]

        # Run the stopservice.sh script with the ports as arguments
        subprocess.call(["./stopservice.sh"] + ports)

        return jsonify({'message': 'Shell script executed successfully.'}), 200
    
    except subprocess.CalledProcessError as e:
        return jsonify({'message': 'Failed to execute shell script.', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
