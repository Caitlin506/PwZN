import argparse
import requests
from bs4 import BeautifulSoup
import json

parser = argparse.ArgumentParser()
parser.add_argument("file_name", help="name of created json file")
args = parser.parse_args()

name = args.file_name+".json"
req = requests.get('https://en.wikipedia.org/wiki/Index_of_feminism_articles')
status = req.status_code

print("Status code = ", status)
print("Information will be saved into: ", name)

soup = BeautifulSoup(req.text,'html.parser')
articles = soup.find('div', {'class': 'mw-parser-output'})

feminism_articles = []

for article in articles.find_all('a'):
    try:
        reference = article['href']
        title = article['title']
        if (title,reference) not in feminism_articles:
            feminism_articles.append((title,reference))
    except:
        pass

with open(name, 'w') as f:
    json.dump(feminism_articles, f)