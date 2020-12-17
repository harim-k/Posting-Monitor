
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver

import time
import datetime
import os
import difflib
from filecmp import cmp

from messenger import send_message


MONITORING_TIME_INTERVAL = 10
FILES_DIR = 'files'

checked_hrefs = dict()


def _get_current_time():
    """ get current time as string """
    
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


def _get_html_from_url(driver, url):
    """ get html from url """
    
    driver.get(url)
    time.sleep(1)
    for _ in range(10):
        driver.execute_script('window.scrollBy(0,10000)')
        
    page_source = driver.page_source
    html = str(BeautifulSoup(page_source, "html.parser"))

    return html


def _get_hrefs_from_html(html):
    """ get href list form html """

    hrefs = []
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all('a', href=True)

    for anchor in anchors:
        href = anchor['href']
        hrefs.append(href)
    
    return hrefs


def _get_hrefs_from_diff_file(file_name):
    """ get hrefs list from diff file """

    hrefs = []
    with open(file_name, 'r', -1, 'utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == '>':
                hrefs.extend(_get_hrefs_from_html(line))

    return hrefs


def _get_base_url(url):
    """ get base url """

    end_index = -1
    for index, char in enumerate(url[8:], 8):
        if char == '/':
            end_index = index
            break

    return url[:end_index]


def _has_keyword(url, keyword, driver):
    """ return True if url has keyword """

    if not keyword:
        return True
    
    html = _get_html_from_url(driver, url)

    if keyword in html:
        return True
    else:
        return False


def monitor_posting(messenger_type, user, urls, keyword=None):
    """ monitor posting of website """

    driver = webdriver.Chrome()

    # save urls' html as file
    base_url = ['']
    for index, url in enumerate(urls, 1):
        
        base_url.append(_get_base_url(url))
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

        html = _get_html_from_url(driver, url)
        _write_file(html_file_name, html)
        hrefs = _get_hrefs_from_html(html)

        for href in hrefs:
            if href[0] == '/':
                href = base_url[index] + href
            checked_hrefs[href] = True
        

    # monitor posting
    while True:
        for index, url in enumerate(urls, 1):
            dir_name = os.path.join(FILES_DIR, str(index))
            html_file_name = os.path.join(dir_name, 'html.txt')
            new_html_file_name = os.path.join(dir_name, 'new_html.txt')
            diff_file_name = os.path.join(dir_name, 'diff.txt')
            links_file_name = os.path.join(dir_name, 'links.txt')
            diffs_file_name = os.path.join(dir_name, 'diffs.txt')

            new_html = _get_html_from_url(driver, url)
            _write_file(new_html_file_name, new_html)
            
            # make diff file
            os.system(f'diff {html_file_name} {new_html_file_name} > {diff_file_name}')

            hrefs = _get_hrefs_from_diff_file(diff_file_name)
            links = []
            
            # get link list from href list
            for href in hrefs:
                if href[0] == '/':
                    href = base_url[index] + href
                if url in href and href not in checked_hrefs.keys():
                    checked_hrefs[href] = True
                    if _has_keyword(href, keyword, driver):
                        links.append(href)

            print(_get_current_time())
            if links:
                print('Posting Uploaded !!')
            else:
                print('No Posting Uploaded !!')


            # send message to user
            for i in range(len(links)):
                
                print(links[i])
                send_message(messenger_type, user, links[i])

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

