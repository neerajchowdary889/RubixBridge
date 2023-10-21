import requests

# Define the API endpoint URL
api_url = 'http://localhost:20000/api/createdid'  # Replace with the actual API URL

# Define the form data as a dictionary
form_data = {'did_config': {'type':0, 'dir':'', 'config':'', 'master_did':'', 'secret':'My DID Secret', 'priv_pwd':'mypassword', 'quorum_pwd':'mypassword','img_file':'', '', 'priv_img_file':'',  'pub_key_file':'', 'priv_key_file':'', 'quorum_pub_key_file':'', 'quorum_priv_key_file':''}}

# Send a POST request with the form data
try:
    response = requests.post(api_url, data=form_data)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        print("POST request was successful.")
        print("Response content:", response.text)
    else:
        print(f"POST request failed with status code {response.status_code}")
        print("Response content:", response.text)

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
