from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import re
import csv
from selenium import webdriver

df = pd.read_csv('D:\\result1.csv')

scraped_data = []

path = "C:/chromedriver.exe"
browser = webdriver.Chrome(executable_path=path)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'
}

def scrape_manufacturer(soup):
    try:
        manufacturer = soup.find('table', id='productDetails_techSpec_section_1', class_='a-keyvalue prodDetTable').find_all('td', class_='a-size-base prodDetAttrValue')[1].text.strip()
    except:
        manufacturer = soup.find('div', id='detailBullets_feature_div').find_all('span')[8].text
    manufacturer = re.sub(r'[^\x20-\x7E]', '', manufacturer)
    return manufacturer

def scrape_additional_descriptions(soup):
    description_list = []
    descriptions = soup.find('ul', class_='a-unordered-list a-vertical a-spacing-mini').find_all('li')
    for li in descriptions:
        description_text = li.span.text.strip()
        description_list.append(description_text)
    return description_list

def extract_data_asin(url):
    regex_pattern = r'/dp/([A-Z0-9]+)'
    match = re.search(regex_pattern, url)
    if match:
        return match.group(1)
    else:
        return None

for url in df.url[1:201]:
    try:
        complete_url = 'https://www.amazon.in/' + url

        browser.get(complete_url)

        html = browser.page_source

        soup = BeautifulSoup(html, 'lxml')

        manufacturer = scrape_manufacturer(soup)
        additional_description = scrape_additional_descriptions(soup)
        data_asin = extract_data_asin(browser.current_url)

        scraped_info = {
            'URL': complete_url,
            'Manufacturer': manufacturer,
            'Additional Descriptions': additional_description,
            'Data ASIN': data_asin
        }

        scraped_data.append(scraped_info)

    except Exception as e:
        print(f"Error scraping URL: {complete_url}")
        print(str(e))
        continue

scraped_df = pd.DataFrame(scraped_data)
scraped_df.to_csv('scraped_data.csv', index=False)
browser.quit()
