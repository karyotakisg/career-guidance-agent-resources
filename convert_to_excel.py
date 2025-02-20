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
    with open('masters/masters2.json',encoding='utf-8-sig') as f:
        data = json.load(f)
    data = pd.DataFrame(data)
    data.drop(columns=['number_of_students','tag'], inplace=True)
    data = data[~data['university'].str.match(r'^[A-Za-z]')]
    data = data[~data['university'].str.contains('Πανεπιστήμιο Λευκωσίας')]
    data['tuition'] = data['tuition'].astype(str)
    data['duration'] = data['duration'].astype(str)
    data = data[~(data['tuition'].str.contains('εξάμηνα') | data['tuition'].str.contains('Εξάμηνα'))]
    data['tuition'] = data['tuition'].str.replace('euro', '')
    data = data[~data['tuition'].str.contains('Με δίδακτρα')]
    data['tuition'] = data['tuition'].str.replace('.', '0')
    data['duration'] = data['duration'].str.replace('.', '0')
    data['tuition'] = data['tuition'].astype(int)
    data['duration'] = data['duration'].astype(int)
    data['duration'].rename('duration (semesters)', inplace=True)

    

    data.to_excel('masters/masters.xlsx',index=False)