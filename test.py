
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
from filecmp import cmp
import difflib

url1 = 'https://docs.google.com/document/d/1i9j_XGRqFNHX-nu3ehOQ3RgUpLCHNtctCXrXTNKMGVw/edit'
url2 = 'http://acebedmall.co.kr/front/search/categorySearch.do?searchYn=N&ctgNo=2'
url = 'https://blog.naver.com/harim9355'
urls = [url]

driver = webdriver.Chrome()


def _get_html_from_url(url):
    """ get html from url """
    driver.get(url)
    page_source = driver.page_source
    html = str(BeautifulSoup(page_source, "html.parser"))

    return html


def _save_html_as_file(html, file_name):
    """ save html as file """
    with open(file_name, 'w', -1, 'utf-8') as f:
        f.write(html)


def _get_link_from_html(html):
    """ get link form html """
    links = []
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all('a', href=True)

    for anchor in anchors:
        links.append(anchor['href'])
    
    return links


def _get_link_from_diff_file(file_name):
    """ get link from diff file """
    links = []
    with open(file_name, 'r', -1, 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == '>':
                links.extend(_get_link_from_html(line))

    return links



# save urls' html as file
for index, url in enumerate(urls, 1):
    file_name = 'naver2.txt'

    html = _get_html_from_url(url)
    _save_html_as_file(html, file_name)


