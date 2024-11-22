from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import pandas as pd
import requests


# Initialize the WebDriver (Chrome in this case)
driver = webdriver.Chrome()

# Navigate to the URL of your webpage
driver.get("https://masters.minedu.gov.gr/Masters/search/en")  # Replace with the actual URL

# Locate the dropdown element by its 'name' attribute
dropdown = driver.find_element(By.NAME, 'masters_table_length')

# Create a Select object and interact with the dropdown
select = Select(dropdown)

# Select the option with value "-1" (which is the "All" option)
select.select_by_value("-1")
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Extract all <td> elements
td = soup.find_all('td')
text = [i.get_text() for i in td]
text = [i for i in text if i != '']

# Separate Masters and Universities into separate lists
masters = [text[i] for i in range(len(text)) if i % 2 == 0]
masters = [i.title() for i in masters]  # Capitalize each word in the 'masters' list
masters = [i.strip() for i in masters]
universities = [text[i] for i in range(len(text)) if i % 2 != 0]
universities = [i.title() for i in universities]  # Capitalize each word in the 'universities' list

# Extract all links
links = soup.find_all('a', href=True)
master_links = [i['href'] for i in links if '/Masters/viewMaster/' in i['href']]

# Create DataFrame
df = pd.DataFrame({'masters': masters, 'universities': universities, 'links': master_links})

# Adjust the column names
df.columns = ['Master', 'University', 'Link']

uni_website = []
for link in master_links:
    page = requests.get(link)
    page_soup = BeautifulSoup(page.content, 'html.parser')
    uni_website_tag = page_soup.find_all('a')
    for tag in uni_website_tag:
        if "Master's website" in tag.text:
            uni_website_tag = tag['href']
            uni_website.append(uni_website_tag)
            break
df = pd.DataFrame({'Master': masters, 'University': universities, 'Gov Link': master_links, 'University Website': uni_website})
df.sort_values('Master', inplace=True)

chunk_size = 100

# Split DataFrame into chunks
chunks = [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]

# Save each chunk to a separate text file
#for idx, chunk in enumerate(chunks):
#    filename = f'data_chunk_{idx + 1}.txt'  # e.g., data_chunk_1.txt, data_chunk_2.txt
#    chunk.to_csv(filename, sep='\t', index=False)

# Save DataFrame to a text file
df.to_csv('data.txt', sep='\t', index=False, encoding='utf-8-sig')
