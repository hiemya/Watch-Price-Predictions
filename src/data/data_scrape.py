from bs4 import BeautifulSoup
from requests_html import HTMLSession
import numpy as np


s = HTMLSession()
start = 'https://www.chrono24.com/omega/index.htm?goal_suggest=1&goal_suggest=1'

def geturl(start):
    r = s.get(start)
    soup = BeautifulSoup(r.text, 'lxml')
    html_block = soup.find('div', {'class': 'article-list article-list-watches block'})
    watches = [link['href'] for link in html_block.find_all('a')]
    links = ['https://www.chrono24.com' + x for x in watches]
    return (links)

def getdata(url):
    raw_data = np.array([])
    data = []
    content = s.get(url)
    soup = BeautifulSoup(content.text, 'lxml')
    # retrieve watch prices
    prices = soup.find('span', {'class': 'currency'}).next_sibling
    clean_text = ''
    for price in prices:
        clean_text = clean_text + price

    data.append(clean_text)

    section = soup.find('section', {'id': 'jq-specifications'})
    children = section.find_all(lambda tag: tag.name == 'td' and not tag.attrs)
    for child in children:
        # data.append(child.text)
        clean_text_remove = child.text.replace('\n', "")
        clean_text = clean_text_remove.strip()
        data.append(clean_text)
    raw_data = (raw_data, data)
    return raw_data

while True:
    links = geturl(start)
    for link in links:
        getdata(link)
