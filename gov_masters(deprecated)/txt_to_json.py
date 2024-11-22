import json

# Function to read data from a text file and convert to JSON
def txt_to_json(file_path):
    # Open and read the txt file
    with open(file_path, "r", encoding="utf-8-sig") as file:
        # Read all lines
        txt_data = file.read()

    # Split the text into rows
    rows = txt_data.strip().split("\n")

    # Extract column names (headers)
    headers = rows[0].split("\t")

    # Create an empty list to store the JSON objects
    data = []

    # Iterate through the rest of the rows and convert each one to a dictionary
    for row in rows[1:]:
        columns = row.split("\t")
        record = dict(zip(headers, columns))  # Zip the header with row values
        data.append(record)

    # Convert the list to JSON
    json_data = json.dumps(data, indent=4)

    # Save the JSON data to a file (optional)
    with open("masters_programs.json", "w", encoding="utf-8-sig") as json_file:
        json_file.write(json_data)

    # Return the JSON data for further use (optional)
    return json_data

# Call the function with your data.txt file
json_output = txt_to_json("data.txt")

