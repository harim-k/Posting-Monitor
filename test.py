
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
keywords = ['']
keyword = ''
# driver = webdriver.Chrome()

if not keyword:
    print('dd')