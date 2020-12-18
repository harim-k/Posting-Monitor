
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

checked_hrefs = dict()


def _get_current_time():
    """ get current time as string """
    
    current_time = str(datetime.datetime.now())

    return current_time


def _get_html_from_url(driver, url):
    """ get html from url """
    
    driver.get(url)

    while url != driver.current_url:
        time.sleep(10)

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


def monitor_posting(messenger_type, user, urls, keywords):
    """ monitor posting of website """

    driver = webdriver.Chrome()

    # check first hrefs
    base_url = ['']
    for index, (url, keyword) in enumerate(zip(urls, keywords), 1):
        
        base_url.append(_get_base_url(url))

        html = _get_html_from_url(driver, url)
        hrefs = _get_hrefs_from_html(html)

        for href in hrefs:
            if len(href) > 0 and href[0] == '/':
                href = base_url[index] + href
            checked_hrefs[href] = True
        

    # monitor posting
    while True:
        for index, (url, keyword) in enumerate(zip(urls, keywords), 1):

            new_html = _get_html_from_url(driver, url)
            hrefs = _get_hrefs_from_html(new_html)
            links = []
            
            # get link list from href list
            for href in hrefs:
                # print('href : ', href)
                if len(href) > 0 and href[0] == '/':
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
            for link in links:
                print(link)
                send_message(messenger_type, user, link)

            
            # sleep for monitoring time interval
            time.sleep(MONITORING_TIME_INTERVAL)

