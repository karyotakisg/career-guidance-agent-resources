from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import json
import os
from dotenv import load_dotenv

with open('sitemap-undergradprograms.xml', 'r') as f:
    data = f.read()

Bs_data = BeautifulSoup(data, "xml")
urls = Bs_data.find_all('url')
urls = [url.find('loc').text for url in urls]

url = 'https://www.eduguide.gr'
driver = webdriver.Chrome()
driver.get(url) 
time.sleep(2)
login_link = driver.find_element(By.CSS_SELECTOR, 'a.nav-link.hover-gray-button')  
login_link.click()
username_field = driver.find_element(By.ID, 'id_username')  
password_field = driver.find_element(By.ID, 'id_password')  


load_dotenv('./../.env')

username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')

username_field.send_keys(username)
password_field.send_keys(password)


password_field.send_keys(Keys.RETURN)
time.sleep(2)

undergrad = []
for url in urls:
    print(url)
    driver.get(url) 
    time.sleep(1)   
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    infos_json = {}
    
    infos_json['university'] = soup.find('h4',class_='program-school undergrad-program-school').text.strip()
    infos_json['department'] = soup.find('h2',class_='program-title undergrad-program-title').text.strip()
    infos_json['field'] = [field.text.strip() for field in soup.find_all('span',class_='label programinfolabel')]
    infos_json['city'] = soup.find_all('div', class_='col-18 col-md-11 col-lg-12')[3].get_text(strip=True) \
        if len(soup.find_all('div', class_='col-18 col-md-11 col-lg-12')[3].get_text(strip=True).split(',')) == 1 \
        else soup.find_all('div', class_='col-18 col-md-11 col-lg-12')[2].get_text(strip=True)
    
    directions_html = soup.find_all('div', class_='programlabels col-18 col-md-7 col-lg-6')[4].find_next_sibling().find('p') if len(soup.find_all('div', class_='programlabels col-18 col-md-7 col-lg-6'))>=5 else None
    if directions_html:
        infos_json['paths'] = [line.strip() for line in directions_html.text.split('<br>')]
    rows = soup.find_all('ul', class_='exams-row row')

    infos_json['scientific_fields'] = rows[0].find('li', class_='exams-row-info col-9').get_text(strip=True) if len(rows) > 0 else None
    infos_json['general_lyceum_base_score'] = rows[1].find('li', class_='exams-row-info col-9').get_text(strip=True) if len(rows) > 1 else None
    if infos_json['general_lyceum_base_score'] == None:
        continue
    infos_json['vocational_lyceum_base_score'] = rows[2].find('li', class_='exams-row-info col-9').get_text(strip=True) if len(rows) > 2 else None
    infos_json['admitted_students'] = rows[3].find('li', class_='exams-row-info col-9').get_text(strip=True) if len(rows) > 3 else None
    infos_json['ebe_coefficient'] = rows[4].find('li', class_='exams-row-info col-9').get_text(strip=True) if len(rows) > 4 else None
    infos_json['ebe_general_lyceum'] = rows[5].find('li', class_='exams-row-info col-9').get_text(strip=True) if len(rows) > 5 else None
    infos_json['ebe_vocational_lyceum'] = rows[6].find('li', class_='exams-row-info col-9').get_text(strip=True) if len(rows) > 6 else None

    preview = soup.find_all('div', class_='panel-body collapsible-item-preview')
    text = soup.find_all('div', class_='panel-body collapsible-item-body ver-2')
    infos_json['goals'] = preview[0].get_text(strip=True) + text[0].get_text(strip=True) if len(preview) > 0 and len(text) > 0 else None
    
    curriculum_parent = soup.find('div', class_='undergrad-curriculum')
    lists = curriculum_parent.find_all('li')
    curriculum_text = curriculum_parent.find_all('p')
    
    concat_list = ''.join([li.get_text(strip=True) for li in lists])
    concat_text = ''.join([p.get_text(strip=True) for p in curriculum_text])

    #TODO make it a legit cohesive text
    infos_json['curriculum'] = concat_list + concat_text
    
    lab_sections = text[1].find_all('ul') if len(text) > 1 else None
    if lab_sections:
        all_labs = []
        for section in lab_sections:
            labs = [li.get_text(strip=True) for li in section.find_all('li')]
            all_labs.extend(labs)
        infos_json['labs'] = all_labs
    else:
        infos_json['labs'] = None

    infos_json['edu_guide_url'] = url
    infos_json['department_url'] = soup.find('a', class_='undergradprogram_info_webpage_link').get('href') if soup.find('a', class_='undergradprogram_info_webpage_link') else None
    undergrad.append(infos_json)


with open('undergraduates3.json', 'w', encoding='utf-8') as json_file:
    json.dump(undergrad, json_file, ensure_ascii=False, indent=4)

driver.quit()
