import json

with open('mapping_masters.json', 'r', encoding='utf-8-sig') as f:
    mapping = json.load(f)

with open('masters/masters2.json', 'r', encoding='utf-8-sig') as f:
    masters = json.load(f)

with open('masters_not_mapped.txt', 'w', encoding='utf-8') as f:
    for item in masters:
        if item['website'] not in mapping.keys() and item['website']:
            f.write(item['website'])
            f.write('\n')
    