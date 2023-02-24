# Author: Emma Liu
# Date: 2023/2/23 22:28
# Script name:  Web_scapping

# import inline as inline
from lib2to3.pgen2 import driver

from bs4 import BeautifulSoup  # For HTML parsing
from time import sleep         # To prevent overwhelming the server between connections
from requests import get
from selenium import webdriver # API that allows you to programmatically interact with a browser the way a real user would.
from selenium.webdriver.common.keys import Keys
# driver.get("https://condos.ca")
import pandas as pd
import os
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
#
# os – for accessing our folder structures
# time – for putting sleep functionality which will pause our code for a few seconds
# selenium – for automating website navigation flow and downloading HTML content
# bs4 – for extracting relevant data from HTML page source
from selenium import webdriver

driver = webdriver.Chrome()
url = 'https://www.realtor.ca/on/toronto/real-estate-for-sale'
# url = "https://condos.ca"
driver.get(url)


def scrapping_function(current_url, click_next_button):
    driver.get(current_url)
    i = 1
    next_page_true = True
    while next_page_true:
        page = driver.page_source
        file_ = open('saved_pages/toronto/page_{}.html'.format(i), 'w')
        file_.write(page)
        file_.close()
        page_url = driver.current_url
        elem = driver.find_element_by_xpath(click_next_button)
        elem.click()
        time.sleep(2)
        page_url_next = driver.current_url
        if page_url == page_url_next:
            next_page_true = False
        else:
            i += 1

# initializing needed variables

click_next_button = "/html/body/form/div[5]/div[2]/span/div/div[4]/div[3]/span/span/div/a[3]"

# launching firefox wedriver
# binary = FirefoxBinary('Location_for _firefox_installation')
# driver = webdriver.Firefox(firefox_binary=binary)
#
# # calling scrapping function
# scrapping_function(realtor_url, click_next_button)
# driver.close()