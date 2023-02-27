# Author: Emma Liu
# Date: 2023/2/23 22:28
# Script name:  Web_scapping

from lib2to3.pgen2 import driver
from bs4 import BeautifulSoup  # For HTML parsing
from time import sleep         # To prevent overwhelming the server between connections
from requests import get
from selenium import webdriver # API that allows you to programmatically interact with a browser the way a real user would.
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import time
import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# os – for accessing our folder structures
# time – for putting sleep functionality which will pause our code for a few seconds
# selenium – for automating website navigation flow and downloading HTML content
# bs4 – for extracting relevant data from HTML page source


# print(selenium.__version__)

# create an instance of the webdriver class, which represents a browser window.
# launching chrome wedriver
driver = webdriver.Chrome()
url = 'https://www.realtor.ca/on/toronto/real-estate-for-sale'
# url = "https://condos.ca"
## Smaller list- 155: 600K to 1.2Million RH listing
url2= 'https://www.realtor.ca/map#LatitudeMax=43.97778&LongitudeMax=-79.37101&LatitudeMin=43.82935&LongitudeMin=-79.48559&view=list&Sort=6-D&PGeoIds=g30_dpz9b86g&PropertyTypeGroupID=1&PropertySearchTypeId=1&TransactionTypeId=2&PriceMin=600000&PriceMax=1200000&Currency=CAD'
# call the get method on that instance to navigate to a website.
# driver.get(url2)



## Step 1: function to scrap the web page
def scrapping_function(current_url, click_next_button):
    # driver = webdriver.Chrome()
    driver.get(current_url)
    i = 0
    next_page_true = True
    while next_page_true:
        page = driver.page_source # driver.page_source is saving all the HTML content of the page in the variable which is saved as an HTML file in the local folder.
        a=i+1
        file_ = open(r'C:\\Users\PC\Documents\GitHub\Web-scrapping-using-canadian-real-estate-data\file\page_{}.html'.format(a), 'w', encoding='utf-8')
        file_.write(page)
        file_.close()
        page_url = driver.current_url
        wait = WebDriverWait(driver, 600)
        elem = wait.until(EC.visibility_of_element_located((By.XPATH, click_next_button)))
        elem.click()
        time.sleep(2)
        page_url_next = driver.current_url
        if page_url == page_url_next:
            next_page_true = False
        else:
            i += 1
# define the XPath of the "Next" button
click_next_button ='/html/body/form/div[5]/div[2]/span/div/div[4]/div[3]/span/span/div/a[3]' #'//*[@id="ListViewPagination_Bottom"]/div/a[3]'

# # calling scrapping function
scrapping_function(url2, click_next_button)
driver.close()


##Step 2: getting data from each pages
df = pd.DataFrame()

for file in os.listdir('C:/Users/PC/Documents/GitHub/Web-scrapping-using-canadian-real-estate-data/file'):
    html_file = r'C:/Users/PC/Documents/GitHub/Web-scrapping-using-canadian-real-estate-data/file/{}'.format(file)
    soup = BeautifulSoup(open(html_file, encoding='utf-8'), "html.parser")
    data = soup.find_all(class_="cardCon")
    for i, elem in enumerate(data):
        price = data[i].find(class_="listingCardPrice").get_text()
        address = data[i].find(class_="listingCardAddress").get_text()
        rooms = data[i].find_all(class_="listingCardIconNum")
        bedrooms = rooms[0].get_text()
        bathrooms = rooms[1].get_text()
        try:
            row_df = pd.DataFrame({'price': [price],
                                   'address': [address],
                                   'bedrooms': [bedrooms],
                                   'bathrooms': [bathrooms],
                                   'page': [file]})
            df = pd.concat([df, row_df])
            del row_df
        except:
            print("Error in record_{}".format(i))


# cleaning dataframe
def cleaning_address(x):
    return (x.replace("\n", "").strip())


df['address'] = df['address'].apply(cleaning_address)

# saving data file
df.to_csv(r'C:/Users/PC/Documents/GitHub/Web-scrapping-using-canadian-real-estate-data/output/toronto.csv'\
          , index=False)