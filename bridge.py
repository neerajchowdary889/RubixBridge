from flask import Flask, request, jsonify, Response
import requests,json, time, geocoder, sys
from flask_cors import CORS
from pymongo import MongoClient

# Define MongoDB connection information
MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "jm"

app = Flask(__name__)
CORS(app)

def security(fname):
	APILog={'timestamp':int(time.time()),
		'location': geocoder.ip(str(request.environ['REMOTE_ADDR'])).city,
		'clientAgent':str(request.headers.get('User-Agent')),
		'clientIP':str(request.environ['REMOTE_ADDR']),
		'API':fname}
	mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
	db = mongo_client[MONGO_DB]
	MONGO_COLLECTION = "RubixBridgeAPILOG"
	collection = db[MONGO_COLLECTION]
	collection.insert_one(APILog)
	mongo_client.close()

#CreateDID Parent API
@app.route('/api/createparentdid', methods=['GET'])
def createParentDID():
	security(str(sys._getframe().f_code.co_name))
	print("createDID API")
	mongo_client = MongoClient(MONGO_HOST, MONGO_PORT)
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
        # Request was successful
			message = json.loads(response.text)
			if message['status'] == True:
				print(message['result']['did'])
				print(message['result']['peer_id'])
				didpeerid={'status':True,'createTime':end_time,'port':port,'did':str(message['result']['did']),'peerid':str(message['result']['peer_id']),'timeTaken':elapsed_time,'creatorIP':request.environ['REMOTE_ADDR'],'creatorLocation':geocoder.ip(str(request.environ['REMOTE_ADDR'])).city}
				print(didpeerid)
				collection.insert_one(didpeerid)
				mongo_client.close()
				
				return didpeerid
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
    
#CreateDID Child API
@app.route('/api/createchilddid', methods=['GET'])
def createchildDID():
    print("createDID API")

    # Get the user input for the field (e.g., "AM" or "ISK")
    user_input = request.args.get('app', '')

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
                didpeerid={'status':True, 'did':message['result']['did'],'peerid':message['result']['peer_id'],'timeTaken':elapsed_time}
                return didpeerid
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
    print("GetallDID API")

     # Get the user input for the field (e.g., "AM" or "ISK")
    user_input = request.args.get('app', '')

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
        # Add more field-to-port mappings as needed
    }

    # Default port (if the user input is not recognized)
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

@app.route('/api/createdt')
def createdt():
    print("createDT")
    url = 'http://localhost:20000/api/create-data-token?did=bafybmiapskapvyjxa4zaa3hvzuqiu6sti7h6aofam6eu7vxjef3ad4lg7m'
    form_data = {'UserID': '1','UserInfo': 'abc','CommitterDID': 'bafybmiapskapvyjxa4zaa3hvzuqiu6sti7h6aofam6eu7vxjef3ad4lg7m','BacthID': '1','FileInfo': '{}'}
    files = {'FileContent': ('quorumlist.json', open('quorumlist.json', 'rb'), 'application/json')}

    try:
        response = requests.post(url, data=form_data, files=files)
        print(response.text)
        
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        return (str(e))

@app.route('/api/commitdt', methods=['GET'])
def commitdt():
    print('commitDT')
    url = 'http://localhost:20000/api/commit-data-token?did=bafybmiapskapvyjxa4zaa3hvzuqiu6sti7h6aofam6eu7vxjef3ad4lg7m&batchID=1'
    response = requests.post(url)
    print(response.text)
    return json.loads(response.text)

@app.route('/api/shutdownall')
def shutdownall():
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
            # print(port, response.status_code)
            if response.status_code == 200:
                node_statuses[node_name] = "Shutdown complete"
            else:
                node_statuses[node_name] = "Unable to connect (Node may be down)"
        except requests.exceptions.RequestException as e:
            node_statuses[node_name] = f"Unable to connect (Error: {str(e)})"

    return jsonify(node_statuses)

@app.route('/api/testallnodes', methods=['GET'])
def testAllNodes():
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
