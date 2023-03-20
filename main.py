import requests
import json
import time
import os
from bs4 import BeautifulSoup
from login import cookies, headers, data

USER = 'vlad_bb@icloud.com'
PASSWORD = '7184014'



class Scrapper:
    """Класс парсера"""

    def __init__(self):
        self.base_url = 'https://www.tesmanian.com/'
        self.news_ulr = 'https://www.tesmanian.com/blogs/tesmanian-blog'
        self.login_url = 'https://www.tesmanian.com/account/login'
        self.session = requests.Session()
        self.response = None
        self.storage = 'data/storage.json'
        self.all_records = None
        self.fresh_news = list()

    def login(self) -> None:
        """Процес авторизації"""
        data['customer[email]'] = USER
        data['customer[password]'] = PASSWORD
        self.response = self.session.post(self.login_url, cookies=cookies, headers=headers, data=data)
        if self.response.status_code == 200:
            print(f'Successes, status 200')
        else:
            print(f'Something wrong, status {self.response.status_code}')

    def get_articles(self) -> dict:
        """Отримуємо список всіх новин"""
        articles = dict()
        response = self.session.get(self.news_ulr)
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            cards = soup.find('div', class_='blog-posts').find_all('div', class_="blog-post-card__info")
            print(f'Collected: {len(cards)}')
            for card in cards:
                obj: bs4.element.Tag = card.find('p', class_='h3')
                if obj:
                    link = self.base_url + obj.find('a').get('href')
                    title = obj.text
                    articles[link] = title
                    print(f'Article was added to dict: {title}')
        except Exception as err:
            print(f'Error: {err}')
        return articles

    def check_news(self) -> list[dict]:
        """Функція перевірки нових новин яких ще немає в сховищі"""
        articles = self.get_articles()
        if not os.path.exists(self.storage):
            with open(self.storage, 'w', encoding='utf-8') as fd:
                json.dump({}, fd, ensure_ascii=False, indent=4)
        with open(self.storage, 'r+', encoding='utf-8') as file:
            self.all_records = json.load(file)
            for key, value in articles.items():
                if self.all_records.get(key) is None:
                    self.fresh_news.append({key: value})
                    print(f'Fresh news was appended')
            self.all_records.update(articles)
            file.seek(0)
            json.dump(self.all_records, file, ensure_ascii=False, indent=4)
            file.truncate()
        return self.fresh_news


if __name__ == '__main__':
    sc = Scrapper()
    sc.login()
    sc.check_news()
    time.sleep(5)
    sc.check_news()

