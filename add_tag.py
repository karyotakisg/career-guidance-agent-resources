import json
import sys
# Adds a tag to each item in the JSON file, to track it it is undergraduate or masters program

choice = sys.argv[1]
if choice == 'undergraduates':
    file = 'undergraduates/undergraduates2.json'
elif choice == 'masters':
    file = 'masters/masters2.json'
else:
    print("Invalid choice. Please choose 'undergraduates' or 'masters'.")
    sys.exit(1)

with open(file, 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for item in data:
    item["tag"] = "undergraduates"
with open('undergraduates/undergraduates2_with_tag.json', 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)