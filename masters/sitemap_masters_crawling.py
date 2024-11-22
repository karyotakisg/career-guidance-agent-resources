from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import time
import json
from dotenv import load_dotenv
import os

with open('sitemap-gradprograms.xml', 'r') as f:
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

masters = []
for url in urls:
    driver.get(url) 
    time.sleep(1)   
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    info = soup.find_all(class_='col-md-12 col-lg-13 col-xl-14')
    infos_json = {}
    
    infos_json['university'] = info[0].text.strip() if len(info) > 0 else None
    infos_json['department'] = info[1].text.strip() if len(info) > 1 else None
    infos_json['master'] = info[2].text.strip() if len(info) > 2 else None
    infos_json['tuition'] = info[3].text.strip() if len(info) > 3 else None
    infos_json['duration'] = info[4].text.strip() if len(info) > 4 else None
    infos_json['attendance'] = info[5].text.strip() if len(info) > 5 else None
    infos_json['number_of_students'] = info[6].text.strip() if len(info) > 6 else None
    infos_json['website'] = info[8].find('a')['href'] if len(info) > 8 else None
    infos_json['edu_guide_url'] = url

    driver.get(url+'/curriculum') 
    time.sleep(0.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    curriculum = soup.find(class_='entry-content')
    infos_json['curriculum'] = curriculum.text.strip() if curriculum else None
    masters.append(infos_json)
with open('programs_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(masters, json_file, ensure_ascii=False, indent=4)

driver.quit()
