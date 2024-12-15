import json

with open('undergraduates/undergraduates.json', 'r', encoding='utf-8-sig') as f:
    undergraduates = json.load(f)

for item in undergraduates:
    if 'paths'  in item:
        item['paths'] = ', '.join(item['paths'])
    item['field'] = ', '.join(item['field'])

with open('undergraduates/undergraduates2.json', 'w', encoding='utf-8-sig') as f:
    json.dump(undergraduates, f, indent=4, ensure_ascii=False)