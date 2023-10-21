from flask import Flask, request, jsonify, Response
import requests, time
import json


app = Flask(__name__)

@app.route('/createdid')
def createDID():
    # Define the API endpoint URL
    url = 'http://localhost:20000/api/createdid'

    # Create a dictionary for form data
    form_data = {'did_config': (None, '{"type":0,"dir":"","config":"","master_did":"","secret":"My DID Secret","priv_pwd":"mypassword","quorum_pwd":"mypassword"}'),}

    # Specify the file to upload
    files = {'img_file': ('image.png', open('image.png', 'rb'), 'image/png')}

# Send a POST request with multipart/form-data
    try:
        response = requests.post(url, data=form_data, files=files)
    
    # Check the response status code
        if response.status_code == 200:
        # Request was successful
            message = response.text
            print("POST request was successful.")
            print("Response content:", message)
            if message['status'] == true:
                print(message['result']['did'])
                print(message['result']['peer_id'])
                didpeerid={'did':message['result']['did'],'peerid':message['result']['peer_id']}
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
        return (str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)