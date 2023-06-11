#!/usr/bin/python3
import datetime
import pymysql
import requests


# https://www.newsminimalist.com/
news_headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh2eHdlZnNjdWVwaW5naG1sdmxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzkzNDQ0NjIsImV4cCI6MTk5NDkyMDQ2Mn0.eZLOeKKgFt3Gfu63L2vpV86ImWVLO9OqJ6sdRrCrFEE',
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
          'Apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh2eHdlZnNjdWVwaW5naG1sdmxvIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzkzNDQ0NjIsImV4cCI6MTk5NDkyMDQ2Mn0.eZLOeKKgFt3Gfu63L2vpV86ImWVLO9OqJ6sdRrCrFEE'}


def url_date_params():
    today = datetime.datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    yesterday = (today - datetime.timedelta(days=1))
    date_str = yesterday.strftime("%Y-%m-%d")
    return date_str, today_str


def filter_news(rating:float, title:str):
    filter = rating < 6
    if filter:
        title_lower = title.lower()
        filter = not ("rwa" in title_lower or "real world assets" in title_lower)
    return filter


def save_news(title:str, category:str, source:str, rating:float, url:str, date_str:str):
    with pymysql.connect(host='localhost', port=3306, user='ccenlei', password='123', database='web3') as db:
        cursor = db.cursor()
        sql = "INSERT INTO ai_news(title, category, source, rating, url, date_str) VALUES ('%s', '%s',  '%s', '%s',  '%s',  '%s')" \
              % (title, category, source, rating, url, date_str)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            # need logger
            db.rollback()


def crawl_news():
    date_str, today_str = url_date_params()
    news_url = f'https://api.newsminimalist.com/rest/v1/articles?select=title_rewritten_v2%2Curl%2Crating_v2%2Csource%2Ccategory%2Cid%2Ccluster_id&created_at=gte.{date_str}T12%3A00%3A00.000Z&created_at=lt.{today_str}T12%3A00%3A00.000Z&rating_v2=gte.0&rating_v2=lt.10&order=rating_v2.desc'
    with requests.get(url=news_url, headers=news_headers) as response:
        news = response.json()
        for ele in news:
            title = ele['title_rewritten_v2']
            url = ele['url']
            rating = ele['rating_v2']
            source = ele['source']
            category = ele['category']
            filter = filter_news(rating, title)
            if filter is False:
                save_news(title, category, source, rating, url, date_str)
            else:
                print(source, title)


crawl_news()
