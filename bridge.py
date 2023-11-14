from flask import Flask, request, jsonify, Response
import requests,json, time



app = Flask(__name__)


#CreateDID Parent API
@app.route('/api/createparentdid')
def createParentDID():
    print("createDID API")
    start_time = time.time()
    # Define the API endpoint URL
    url = 'http://localhost:20000/api/createdid'

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
    
#CreateDID Child API
@app.route('/api/createchilddid/<parentDID>')
def createchildDID(parentDID):
    print("createDID API")
    alldid = requests.get('http://localhost:20000/api/getalldid')
    alldid = json.loads(alldid.text)
    parentDID = alldid['account_info'][0]['did']
    print(parentDID)
    start_time = time.time()
    # Define the API endpoint URL
    url = 'http://localhost:20000/api/createdid'

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
@app.route('/api/getalldid')
def getalldid():
    print("GetallDID API")

    url='http://localhost:20000/api/getalldid'

    try:
        response = requests.get(url)

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
        
        return response.text
    except requests.exceptions.RequestException as e:
        return (str(e))

@app.route('/api/commitdt')
def commitdt():
    print('commitDT')
    url = 'http://localhost:20000/api/commit-data-token?did=bafybmiapskapvyjxa4zaa3hvzuqiu6sti7h6aofam6eu7vxjef3ad4lg7m&batchID=1'
    response = requests.post(url)
    print(response.text)
    return response.text



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)


b'{ "data":{ "imei":"869523057983679","uid":1,"dtm":"20231113091405","seq":6621,"sig":24,"msg":"log","modbus": [{ "sid":1,"stat":21,"indx":1,"rcnt":  0 }] }}\r\n'