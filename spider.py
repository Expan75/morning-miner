# standard package imports
import re

# Misc
from bs4 import BeautifulSoup
from requests import get
import pandas as pd

# Selenium Stuff
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# Set up webdriver 
chrome_options = Options()
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path="/Users/Erik/Dev/finscrape/chromedriver", options=chrome_options)

# Utility methods for generating scrapeable page
def getPageRes(url):
    return get(url)

def getSoup(res):
    return BeautifulSoup(res.text, 'html.parser')

# Base url containing list of filtered funds
BASE_URL = 'https://www.morningstar.co.uk/uk/fundscreener/default.aspx?fbclid=IwAR1K8uh6n3uf_xfPmAWYvgbgfhmSeJmpvMECi1lNOYB_9wOEKfh2ssuSoAQ#?filtersSelectedValue=%7B%22categoryId%22:%7B%22id%22:%22EUCA000550%22%7D,%22fundSize%22:%7B%22id%22:%22:BTW:1000000000:10000000000%22%7D,%22geoRegion%22:%7B%22id%22:%22RE_UnitedKingdom%22%7D,%22globalCategoryId%22:%7B%22id%22:%22$GC$UKEQLC%22%7D,%22managementStyle%22:%7B%22id%22:%22true%22%7D,%22totalReturnTimeFrame%22:%7B%22id%22:%22GBRReturnM60%22%7D,%22investmentObjective%22:%7B%22id%22:%22Growth:EQ:1%22%7D%7D&sortField=legalName&sortOrder=asc'

# Navigate to base URL
driver.get(BASE_URL)

def handle_popup():
    """ Utility function for handling popup after every URL hit """

    # Handle query popup radio
    individual_investor_radio_option = driver.find_element_by_id("individualinvestor") # locate right radio btn
    individual_investor_radio_option.click()

    # Submit response 
    accept_btn = driver.find_element_by_id("_evidon-accept-button")
    accept_btn.click()

# # Handle potential popups
handle_popup()

# Get table elements and start loop (for every fund in the paginated 10):
for counter, result in enumerate(range(0,10)):
    continue

# locate i'th fund to click on
# fund_clickable = driver.find_elements_by_class_name("mds-link mds-link--no-underline ec-table__investment-link")
# fund_clickable.click()

# handle popups
handle_popup()