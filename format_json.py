import json

# Adds a tag to each item in the JSON file, to track it it is undergraduate or masters program

with open('undergraduates/undergraduates2.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)
for item in data:
    item["tag"] = "undergraduates"
with open('undergraduates/undergraduates2_with_tag.json', 'w', encoding='utf-8-sig') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)