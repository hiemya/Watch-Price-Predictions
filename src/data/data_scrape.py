from bs4 import BeautifulSoup
from requests_html import HTMLSession
import pandas as pd
import time
import random
from pathlib import Path

s = HTMLSession()


# This function retrieves all the URLs that are being scraped from a given starting point
def get_url(start):
    r = s.get(start)
    soup = BeautifulSoup(r.text, 'lxml')
    html_block1 = soup.find('div', {'class': 'article-list article-list-watches block'})
    html_block2 = html_block1.find_all(attrs={"data-manufacturer": "Rolex"})
    links = []
    for x in html_block2:
        link = 'https://www.chrono24.com' + x.get('href')
        links.append(link)
    return links


# This function retrieves the desired data from a given URL
def get_data(url):
    data = []
    content = s.get(url)
    soup = BeautifulSoup(content.text, 'lxml')
    # retrieve watch prices
    try:
        price = soup.find('span', {'class': 'currency'}).next_sibling.strip()
        data.append(price)
    except:
        price = ""
        data.append(price)

    basic_info = soup.find('section', {'id': 'jq-specifications'})
    try:
        listing_code = basic_info.find("strong", text="Listing code").find_next().get_text()
        data.append(listing_code)
    except:
        listing_code = ""
        data.append(listing_code)
    try:
        model = basic_info.find("strong", text="Model").find_next().get_text()
        data.append(model)
    except:
        model = ""
        data.append(model)
    try:
        movement = basic_info.find("strong", text="Movement").find_next().get_text()
        data.append(movement)
    except:
        movement = ""
        data.append(movement)
    try:
        case_material = basic_info.find("strong", text="Case material").find_next().get_text()
        data.append(case_material)
    except:
        case_material = ""
        data.append(case_material)
    try:
        bracelet_material = basic_info.find("strong", text="Bracelet material").find_next().get_text()
        data.append(bracelet_material)
    except:
        bracelet_material = ""
        data.append(bracelet_material)
    try:
        production_year = basic_info.find("strong", text="Year of production").find_next().get_text()
        data.append(production_year)
    except:
        production_year = ""
        data.append(production_year)
    try:
        condition = basic_info.find("strong", text="Condition").find_next().get_text().strip()
        data.append(condition)
    except:
        condition = ""
        data.append(condition)
    try:
        delivery_scope = basic_info.find("strong", text="Scope of delivery").find_next().get_text().strip()
        data.append(delivery_scope)
    except:
        delivery_scope = ""
        data.append(delivery_scope)
    try:
        gender = basic_info.find("strong", text="Gender").find_next().get_text().strip()
        data.append(gender)
    except:
        gender = ""
        data.append(gender)
    try:
        case_diameter = basic_info.find("strong", text="Case diameter").find_next().get_text().strip()
        data.append(case_diameter)
    except:
        case_diameter = ""
        data.append(case_diameter)

    return data


# Loop that scrapes a set amount of pages from a given starting point
raw_data = []
x = range(0, 250)
for i in range(len(x)):
    start = 'https://www.chrono24.com/rolex/index-{}.htm?query=rolex'.format(x[i])
    links_ = get_url(start)
    for link in links_:
        watch = get_data(link)
        raw_data.append(watch)
    time.sleep(random.randint(6, 30))

raw_df = pd.DataFrame(raw_data)

filepath = Path(
    'C:/Users/yhiemeleers/OneDrive - Deloitte (O365D)/Desktop/Personal/Projects/Watch Price Predictions/data/raw/raw_data.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
raw_df.to_csv(filepath)
