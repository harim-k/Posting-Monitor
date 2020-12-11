# clien_market_parser.py
import requests
from bs4 import BeautifulSoup
import os

# 파일의 위치
# request를 통한 텍스트 긁어오기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('http://www.naver.com')
print(req.text)