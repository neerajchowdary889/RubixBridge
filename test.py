import requests

api_url = 'http://13.235.145.208:5050/api/savedatatoken'
json_data = {
    "key1": "value1",
    "key2": "value2"
}

response = requests.post(api_url, json=json_data)

print(response.status_code)  # Print the HTTP status code
print(response.json())       # Print the response JSON
