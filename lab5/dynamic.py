from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="name of created json file")
args = parser.parse_args()

name = args.file_name+".json"
print("Information will be saved into: ", name)

options = Options()
#options.add_argument('--headless')
options.add_argument('--disable-notifications')

service = Service('chromedriver_linux64/chromedriver')
driver = webdriver.Chrome(service = service, options = options)
driver.get('https://www.goodreads.com/book/popular_by_date/2022/11?ref=nav_brws_newrels')
for i in range(1):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(1)
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#__next > div > main > div.PopularByDatePage__content > div.PopularByDatePage__listContainer > div.PopularByDatePage__paginationSelector > div > div > button')))
    button.click()
    
books = []

elements = driver.find_elements(By.CSS_SELECTOR, '#__next > div > main > div.PopularByDatePage__content > div.PopularByDatePage__listContainer > div.RankedBookList > article > div.BookListItem__body ')
for element in elements:
    title = element.find_element(By.CSS_SELECTOR,'div.BookListItem__title > h3 > strong > a').text
    rating = element.find_element(By.CSS_SELECTOR,'div.BookListItem__beneathTitle > div.BookListItemRating > span > div > div.AverageRating > span.AverageRating__ratingValue > span').text
    books.append(('Title: '+title,'Rating: '+rating))
    
with open(name, 'w') as f:
    json.dump(books, f)

driver.close()

