import pandas as pd
import json
import sys

choice = sys.argv[1]
if choice == 'undergraduates':
    with open('undergraduates/undergraduates2.json',encoding='utf-8-sig') as f:
        data = json.load(f)
    data = pd.DataFrame(data)
    data['department'] = data['university'] + ":  " + data['department']
    df = pd.DataFrame()
    df['department'] = data['department']
    df['department_url'] = data['department_url']
    df['text'] = data['goals'] + '\n' + data['curriculum'] +'\n' + data['labs'].to_string(index=False)
    df['text'] = df['text'].str.encode('utf-8', errors='ignore').str.decode('utf-8', errors='ignore')
    df.to_excel('undergraduates/undergraduates.xlsx',index=False)
elif choice == 'masters':
    with open('masters/masters.json',encoding='utf-8-sig') as f:
        data = json.load(f)
    data = pd.DataFrame(data)
    data['title'] = data['university'] + ":  " + data['master']
    df = pd.DataFrame()
    df['title'] = data['title']
    df['department_url'] = data['website']
    df['text'] = data['curriculum']
    df.to_excel('masters/masters.xlsx',index=False)