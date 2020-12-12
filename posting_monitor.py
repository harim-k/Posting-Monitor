
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
from filecmp import cmp
import difflib

url1 = 'https://docs.google.com/document/d/1i9j_XGRqFNHX-nu3ehOQ3RgUpLCHNtctCXrXTNKMGVw/edit'
url2 = 'http://acebedmall.co.kr/front/search/categorySearch.do?searchYn=N&ctgNo=2'
url = 'https://www.skku.edu/skku/campus/skk_comm/notice01.do'
urls = [url2]

driver = webdriver.Chrome()


def get_html(url):
    driver.get(url)
    page_source = driver.page_source
    html = str(BeautifulSoup(page_source, "html.parser"))

    return html



for index, url in enumerate(urls, 1):
    html = get_html(url)

    # save html to text
    with open(f'{index}.txt', 'w', -1, 'utf-8') as f:
        f.write(html)


while True:
    for index, url in enumerate(urls, 1):
        new_html = get_html(url)
        file_name = f'{index}.txt'
        new_file_name = f'new_{index}.txt'

        with open(new_file_name, 'w', -1, 'utf-8') as f:
            f.write(new_html)

        if cmp(file_name, new_file_name) is False:
            # os.system(f'diff {file_name} {new_file_name} > diff_{index}.txt')
            diff = difflib.Differ()
            a = "aaa\n"
            b = "bbb"
            print(diff.compare(a, b))
            print('Posting Uploaded !!')
            

        time.sleep(10)


"""
import telegram
bot = telegram.Bot(token='123412345:ABCDEFgHiJKLmnopqr-0StUvwaBcDef0HI4jk')
chat_id = bot.getUpdates()[-1].message.chat.id

# 파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))





while True:

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    results = soup.select(".isv-r")


    with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
        before = f_read.readline()
        if before != latest:
            bot.sendMessage(chat_id=chat_id, text='새 글이 올라왔어요!')
        else:
            bot.sendMessage(chat_id=chat_id, text='새 글이 없어요 ㅠㅠ')
        f_read.close()

    with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
        f_write.write(latest)
        f_write.close()

    time.sleep(60) # 60초(1분)을 쉬어줍니다.
"""