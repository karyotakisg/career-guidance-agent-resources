import json
import requests
import sys
from dotenv import load_dotenv
import os

#searchable_fields_1 = ["university","department","field","city","scientific_fields",
#                        "general_lyceum_base_score","vocational_lyceum_base_score","admitted_students","ebe_coefficient",
#                        "ebe_general_lyceum","ebe_vocational_lyceum","goals","curriculum","edu_guide_url"]
#searchable_fields_2 = ["university","department","tuition","duration","master","attendance","number_of_students","website","edu_guide_url","curriculum"]

choice = sys.argv[1]
if choice == 'undergraduates':
    file = 'undergraduates/undergraduates2.json'
    chunk_name = 'undergraduates'
    searchable_fields = ["university","department","city","scientific_fields",
                        "general_lyceum_base_score","vocational_lyceum_base_score","admitted_students","goals","department_url"]
    metadata = ["tag","city"]
elif choice == 'masters':
    file = 'masters/masters.json'
    chunk_name = 'masters'
    searchable_fields = ["university","department","tuition","duration","master","attendance","number_of_students","website","curriculum"]
    metadata = ["tag"]
else:
    print("Invalid choice. Please choose 'undergraduates' or 'masters'.")
    sys.exit(1)

def split_json_array(json_array, chunk_size):
    """
    Split a JSON array into smaller arrays of a specified chunk size.
    """
    return [json_array[i:i + chunk_size] for i in range(0, len(json_array), chunk_size)]


with open(file, 'r', encoding='utf-8-sig') as f:
    current_json = json.load(f)


chunk_size = 10
json_chunks = split_json_array(current_json, chunk_size)

load_dotenv()
api_key = os.getenv('API_KEY')

# API URL and headers
url = f'https://api.voiceflow.com/v1/knowledge-base/docs/upload/table?overwrite=true'
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
                "searchableFields": searchable_fields,
                "metadataFields": metadata
            },
            "items": chunk
             } }
    response = requests.post(url, json=payload, headers=headers)
    print(f"Chunk {i+1}: Response: {response.status_code}, {response.text}")

print("All chunks have been processed.")
