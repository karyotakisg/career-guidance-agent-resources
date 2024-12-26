import json
import re

def extract_tuition(masters):
    for master in masters:
        if master['tuition'] == 'Δωρεάν':
            master['tuition'] = 0
        elif 'Ευρώ' in master['tuition'] or 'ευρώ' in master['tuition']:
            try:
                master['tuition'] = int(master['tuition'].split(' ')[0])
            except:
                master['tuition'] = 1
        elif master['tuition']== 'με δίδακτρα':
            master['tuition'] = 1
        elif 'μήνες' in master['tuition']:
            master['tuition'] = master['master']
            if master['tuition'] == 'Δωρεάν':
                master['tuition'] = 0
            elif 'Ευρώ' in master['tuition'] or 'ευρώ' in master['tuition']:
                try:
                    master['tuition'] = int(master['tuition'].split(' ')[0])
                except:
                    master['tuition'] = 1
            elif master['tuition']== 'με δίδακτρα':
                master['tuition'] = 1
    return masters

def extract_semesters(masters, field='duration'):
    for program in masters:
        duration = program.get(field, '')
        if program['duration'] is not None and field == 'tuition':
            continue
        # Match "X-Y έτη" or "X-Y χρόνια" and convert to semesters
        if type(duration) == str:
            duration = duration.lower()
        if type(duration) == int:
            duration = str(duration)

        match = re.search(r'(\d+)[,-](\d+)\s*(έτη|χρόνια|years)', duration)
        if match:
            min_years = int(match.group(1))
            max_years = int(match.group(2))
            avg_years = (min_years + max_years) / 2
            program['duration'] = round(avg_years * 2)  # Assuming 2 semesters per year
            continue

        # Match "X έτη" or "X χρόνια" (single value)
        match = re.search(r'(\d+)\s*(έτη|χρόνια|years)', duration)
        if match:
            years = int(match.group(1))
            program['duration'] = round(years * 2)  # Assuming 2 semesters per year
            continue

        # Match "Χ έτος" or "X χρόνος" (single value)
        match = re.search(r'(\d+)\s*(ετός|έτος|χρόνος|year)', duration)
        if match:
            years = int(match.group(1))
            program['duration'] = years * 2
            continue

        # Match "X-Y μήνες" and convert to semesters
        match = re.search(r'(\d+)[,-](\d+)\s*(μήνες|months)', duration)
        if match:
            min_months = int(match.group(1))
            max_months = int(match.group(2))
            avg_months = (min_months + max_months) / 2
            program['duration'] = round(avg_months / 6)  # Assuming 6 months per semester
            continue

        # Match "X μήνες" (single value)
        match = re.search(r'(\d+)\s*(μήνες|months)', duration)
        if match:
            months = int(match.group(1))
            program['duration'] = round(months / 6)
            continue

        # Match "X-Y εξάμηνα" (explicit range of semesters)
        match = re.search(r'(\d+)[,-](\d+)\s*(έξάμηνα|εξάμηνα|semesters| ακαδημαϊκά εξάμηνα)', duration)
        if match:
            min_semesters = int(match.group(1))
            max_semesters = int(match.group(2))
            avg_semesters = (min_semesters + max_semesters) / 2
            program['duration'] = round(avg_semesters)
            continue

        # Match "X εξάμηνα" (single value)
        match = re.search(r'(\d+)\s*(έξάμηνα|εξάμηνα|semesters|ακαδημαϊκά εξάμηνα)', duration)
        if match:
            program['duration'] = int(match.group(1))
            continue
            
        # Handle masters with no duration data
        if program['duration'] == '.':
            program['duration'] = 0
            continue

        # Default to None if no match
        if field == 'duration':
            program['duration'] = None
    return masters

if __name__ == '__main__':
    masters = json.load(open('masters/masters.json', 'r', encoding='utf-8-sig'))
    masters = extract_semesters(masters)
    masters = extract_semesters(masters, field='tuition')
    masters = extract_tuition(masters)
    json.dump(masters, open('masters/masters2.json', 'w', encoding='utf-8-sig'), indent=4, ensure_ascii=False)
    counter = 0
    for master in masters:
        if master['duration'] is None:
            print(master['master'])
            counter += 1
    print(f"Found {counter} programs with missing duration")