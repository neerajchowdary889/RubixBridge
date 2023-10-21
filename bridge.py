from flask import Flask, request, jsonify, Response
import requests,json, time



app = Flask(__name__)


#CreateDID API
@app.route('/api/createdid')
def createDID():
    print("createDID API")
    start_time = time.time()
    # Define the API endpoint URL
    url = 'http://localhost:20000/api/createdid'

    # Create a dictionary for form data
    form_data = {'did_config': (None, '{"type":0,"dir":"","config":"","master_did":"","secret":"My DID Secret","priv_pwd":"mypassword","quorum_pwd":"mypassword"}'),}

    # Specify the file to upload
    files = {'img_file': ('image.png', open('image.png', 'rb'), 'image/png')}

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)