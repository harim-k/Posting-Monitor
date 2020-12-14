
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
from filecmp import cmp
import difflib

MONITORING_TIME_INTERVAL = 10
FILES_DIR = 'files'

url1 = 'https://docs.google.com/document/d/1i9j_XGRqFNHX-nu3ehOQ3RgUpLCHNtctCXrXTNKMGVw/edit'
url2 = 'http://acebedmall.co.kr/front/search/categorySearch.do?searchYn=N&ctgNo=2'
url3 = 'https://blog.naver.com/harim9355'
url4 = 'https://everytime.kr/370444'
url5 = 'https://cs.skku.edu/news/recent/list'
url6 = 'https://gall.dcinside.com/board/lists/?id=leagueoflegends4'
urls = [url4, url6]

driver = webdriver.Chrome()

hrefs = dict()


def _get_current_time():
    """ get current time as string """

    import datetime
    current_time = str(datetime.datetime.now())

    return current_time


def _write_file(file_name, content):
    """ write content in file """

    with open(file_name, 'w', -1, 'utf-8') as f:
        f.write(content)


def _write_log_file(file_name, logs):
    """ write log list in file """
    
    current_time = _get_current_time()
    
    with open(file_name, 'a', -1, 'utf-8') as f:
        f.write(current_time + '\n')
        for log in logs:
            f.write(log+'\n')
        f.write('\n')


def _get_html_from_url(url):
    """ get html from url """
    driver.get(url)
    time.sleep(1)
    for _ in range(10):
        driver.execute_script('window.scrollBy(0,10000)')
        
    page_source = driver.page_source
    html = str(BeautifulSoup(page_source, "html.parser"))

    return html


def _get_links_from_html(html):
    """ get link list form html """
    links = []
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all('a', href=True)

    for anchor in anchors:
        href = anchor['href']
        if href not in hrefs.keys():
            hrefs[href] = True
            links.append(href)
    
    return links


def _get_links_from_diff_file(file_name):
    """ get link list from diff file """
    links = []
    with open(file_name, 'r', -1, 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == '>':
                links.extend(_get_links_from_html(line))

    return links


def monitor_posting(urls):
    """ monitor posting of website """

    # save urls' html as file
    for index, url in enumerate(urls, 1):
        
        dir_name = os.path.join(FILES_DIR, str(index))
        html_file_name = os.path.join(dir_name, 'html.txt')
        links_file_name = os.path.join(dir_name, 'links.txt')
        diffs_file_name = os.path.join(dir_name, 'diffs.txt')
        
        # initialize directories and files
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(links_file_name, 'w', -1, 'utf-8') as f:
            pass
        with open(diffs_file_name, 'w', -1, 'utf-8') as f:
            pass

        html = _get_html_from_url(url)
        _write_file(html_file_name, html)
        links = _get_links_from_html(html)

        for link in links:
            hrefs[link] = True
        

    # monitor posting
    while True:
        for index, url in enumerate(urls, 1):
            dir_name = os.path.join(FILES_DIR, str(index))
            html_file_name = os.path.join(dir_name, 'html.txt')
            new_html_file_name = os.path.join(dir_name, 'new_html.txt')
            diff_file_name = os.path.join(dir_name, 'diff.txt')
            links_file_name = os.path.join(dir_name, 'links.txt')
            diffs_file_name = os.path.join(dir_name, 'diffs.txt')

            new_html = _get_html_from_url(url)
            _write_file(new_html_file_name, new_html)
            
            # make diff file
            os.system(f'diff {html_file_name} {new_html_file_name} > {diff_file_name}')

            links = _get_links_from_diff_file(diff_file_name)

            print(_get_current_time())
            if links:
                print('Posting Uploaded !!')
            else:
                print('No Posting Uploaded !!')


            # send message to user
            for i in range(len(links)):
                # if links[i][0] == '/':
                #     links[i] = url + links[i]
                print(links[i])
                # send_message(index, i)

            if links:
                _write_log_file(links_file_name, links)
                with open(diff_file_name, 'r', -1, 'utf-8') as f:
                    diffs = f.readlines()
                _write_log_file(diffs_file_name, diffs)
            
            # update file if html is changed
            if cmp(html_file_name, new_html_file_name) is False:
                os.system(f'rm {html_file_name}')
                os.system(f'mv {new_html_file_name} {html_file_name}')

            
            # sleep for monitoring time interval
            time.sleep(MONITORING_TIME_INTERVAL)


try:
    monitor_posting(urls)
except KeyboardInterrupt:
    driver.quit()
