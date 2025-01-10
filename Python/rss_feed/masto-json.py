import requests
import json

# Define the URL and access token
url = "https://jasette.facil.services/api/v1/statuses"
# Read the access token from a file
with open('.secret/access_token.secret', 'r') as file:
    access_token = file.read().strip() 

# Define the headers
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Define the query parameters
params = {
#    "status": f"{json['title']} {json['content'][:250]}[...] {json['url']} #Actualité #Journalisme #Quebec #Canada {json['tag']}",
    "status":"this is a test",
    "language": "fr"  # Adding the language parameter
}

# Define the JSON payload (if needed, otherwise you can omit this)
data = {
    # Your JSON data here if needed
}

# Make the POST request with query parameters
response = requests.post(url, headers=headers, params=params, json=data)

# Check the response
if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Error:", response.status_code, response.text)

