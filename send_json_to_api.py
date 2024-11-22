import json
import requests
import sys
from dotenv import load_dotenv
import os

choice = sys.argv[1]
if choice == 'undergradute':
    file = 'undergraduates/undergraduates.json'
    chunk_name = 'undergraduates'
else:
    file = 'masters/masters.json'
    chunk_name = 'masters'

def split_json_array(json_array, chunk_size):
    """
    Split a JSON array into smaller arrays of a specified chunk size.
    """
    return [json_array[i:i + chunk_size] for i in range(0, len(json_array), chunk_size)]


with open(file, 'r', encoding='utf-8-sig') as f:
    current_json = json.load(f)


chunk_size = 50 
json_chunks = split_json_array(current_json, chunk_size)

load_dotenv()
api_key = os.getenv('API_KEY')

# API URL and headers
url = "https://api.voiceflow.com/v1/knowledge-base/docs/upload/table"
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": api_key
}

# Post each chunk to the API
for i, chunk in enumerate(json_chunks):
    payload = { "data": {
            "name": f'{chunk_name}_{i+1}',
            "schema": {
                "searchableFields": ["University","Department","City"]
            },
            "items": chunk
        } }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Chunk {i+1}: Response: {response.status_code}, {response.text}")

print("All chunks have been processed.")
