from bs4 import BeautifulSoup as bs4
import requests
import csv

url = 'https://netank.net//' #吉田製作所さんのHP記事をスクレイピングしてみた
res = requests.get(url)
print(res.status_code)

soup = bs4(res.text, "html.parser")
article_list = soup.find("div", {'class' : 'list ect-entry-card front-page-type-index'})
cards = article_list.find_all('a')

result = [['title', 'date', 'url']]

for card in cards:
    title = card.get('title')
    date = card.find("span", {'class' : 'entry-date'}).text
    url = card.get('href')
    result.append([title, date, url])
print(result)

with open('output.csv', 'w', encoding='shift_jis') as file:
    writer = csv.writer(file, lineterminator='\n')
    writer.writerows(result)