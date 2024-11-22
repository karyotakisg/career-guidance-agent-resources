import json
import requests
from bs4 import BeautifulSoup
import os
import re

# Read the JSON data from the file
with open('masters_programs.json', 'r', encoding='utf-8-sig') as file:
    data = json.load(file)  # Load the JSON data from the file directly

# Function to fetch text content from a URL
def fetch_text_from_url(url):
    try:
        # Send a GET request to the URL (bypass SSL verification)
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise an error if the request fails

        # Parse the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text from the body of the page (ignores tags)
        body_text = soup.get_text(separator='\n', strip=True)  # Get plain text
        return body_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to sanitize file names by replacing invalid characters
def sanitize_filename(filename):
    # Replace non-alphanumeric characters with underscores
    return re.sub(r'[\\/*?:"<>|]', '_', filename)

# Directory to store the txt files
output_dir = "output_txt_files"
os.makedirs(output_dir, exist_ok=True)

# Loop through each entry in the JSON data
for index, entry in enumerate(data):
    gov_link = entry["Gov Link"]
    print(f"Processing Gov Link: {gov_link}")
    uni_website = entry["University Website"]

    # Fetch the text content from each link
    gov_text = fetch_text_from_url(gov_link)
    uni_text = fetch_text_from_url(uni_website)

    # Sanitize the master name to avoid invalid characters in the file name
    sanitized_master_name = sanitize_filename(entry['Master'])

    # Save the fetched content into txt files
    if gov_text:
        with open(f"{output_dir}/gov_link_{sanitized_master_name}.txt", "w", encoding="utf-8") as file:
            file.write(gov_text)

    if uni_text:
        with open(f"{output_dir}/uni_website_{sanitized_master_name}.txt", "w", encoding="utf-8") as file:
            file.write(uni_text)

    print(f"Processed entry {index + 1}.")

print("Finished processing all entries.")
