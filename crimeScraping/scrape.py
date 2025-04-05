from bs4 import BeautifulSoup as bs4
import requests
import sqlite3
import os
import time

result = [['title', 'date', 'place', 'type', 'url']]

def scrapeList():
    page = 1

    while True:
        url = f'https://www.bouhan-nippon.jp/topics/page/{page}/'
        res = requests.get(url)
        print(res.status_code)

        if res.status_code != 200 and page == 1: # ページがない場合は終了
            print("ERROR: ページ")
            break

        soup = bs4(res.text, "html.parser")
        article_list = soup.find("ul", {'class' : 'p--postlist'})
        if article_list is None: #記事のリストがない場合は終了
            print("ERROR: 記事のリスト")
            break

        cards = article_list.find_all("li")
        if cards is None: # 記事がない場合は終了
            print("ERROR: 記事")
            break

        for card in cards:
            title = card.find("h3", {'class' : 'p--postlist-title'}).text
            date = card.find("time", {'class' : 'p--postlist-date'}).text
            place = card.find("a", {'class' : 'p--postlist-area'}).text
            type = card.find("a", {'class' : 'p--postlist-category'}).text
            url = card.find("h3", {'class' : 'p--postlist-title'}).find("a").get('href')
            result.append([title, date, place, type, url])
        print(result)

        page += 1
        time.sleep(1) # 1秒待ってから次のページに移動(サーバの負荷軽減のため)

def sqlSetup():
    db = 'crime.db'
    if os.path.exists(db):
        os.remove(db)

    conn = sqlite3.connect(db)
    cur = conn.cursor()

    sqlCreateTable = "create table if not exists crime (title text, date text, place text, type text, url text)"
    cur.execute(sqlCreateTable)
    conn.commit()

    sql = "insert into crime (title, date, place, type, url) values (?, ?, ?, ?, ?)"

    for i in range(1, len(result)):
        cur.execute(sql, (result[i][0], result[i][1], result[i][2], result[i][3], result[i][4]))
    conn.commit()

def main():
    scrapeList()
    sqlSetup()
    print("done")

main()