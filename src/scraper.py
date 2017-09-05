"""
Scraps the hindu archives for articles
"""

import re
from datetime import timedelta, date

import requests as rq
from bs4 import BeautifulSoup

class Scraper(object):
    """
    Scraps the site for news articles
    """

    def __init__(self, start_date, end_date):
        """
        Initializes the scrapper object
        """
        self.__url = "http://thehindu.com/archive/web/%s/"
        self.start_date = start_date
        self.end_date = end_date
        self.content = None

    @staticmethod
    def get_article_id(url):
        """
        Returns the article id from the url
        """
        id_section = url.rsplit("/", 1)[1]
        return id_section.split('.')[0].lstrip('article')

    def get_articles(self):
        """
        Returns a list of news articles to scrap
        """
        st_date = date(*[int(x) for x in self.start_date.split("/")])
        end_date = date(*[int(x) for x in self.end_date.split("/")])

        while st_date <= end_date:
            resp = rq.get(self.__url % (st_date.strftime("%Y/%m/%d")))

            if resp.status_code == 200:
                bsoup = BeautifulSoup(resp.content.decode('utf-8'), 'lxml')
                sections = bsoup.find_all('section', {'id': re.compile(r'section_(\d)+')})
                for sect in sections:
                    section_text = sect.find(
                        'a',
                        {
                            'class': 'section-list-heading'
                        }
                    ).get_text().strip()
                    article_list = sect.find(
                        'ul',
                        {
                            'class': 'archive-list'
                        }).find_all(
                            'li'
                        )
                    for article in article_list:
                        yield {
                            "section": section_text,
                            "title": article.a.get_text().strip(),
                            "url": article.a['href'],
                            "article_id": self.get_article_id(article.a['href']),
                            "article_date": st_date.strftime("%Y-%m-%d")
                        }
            else:
                print("Cannot get articles", self.__url)

            st_date = st_date + timedelta(days=1)

    def get_document(self, url):
        """
        Retrieves the news document given the url
        """
        resp = rq.get(url)
        if resp.status_code == 200:
            d_soup = BeautifulSoup(resp.content.decode('utf-8'), 'lxml')
            div_content = d_soup.find('div', {'id': re.compile(r'content-body-(\d)+-(\d)+')})
            if div_content:
                cont = ""
                for p_tag in div_content.find_all('p'):
                    cont = cont + p_tag.get_text()
            else:
                cont = ""

        if cont == "":
            print("Cannot retrieve content for document", url)

        return cont.strip()
