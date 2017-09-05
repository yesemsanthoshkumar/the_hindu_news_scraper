"""
Scraps the hindu archives for articles
"""

import re
import requests as rq
from bs4 import BeautifulSoup

class Scraper(object):
    """
    Scraps the site for news articles
    """

    def __init__(self, q_date):
        """
        Initializes the scrapper object
        """
        self.__url = "http://thehindu.com/archive/web/%s/" % (q_date)
        self.query_date = q_date
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
        self.resp = rq.get(self.__url)
        if self.resp.status_code == 200:
            bsoup = BeautifulSoup(self.resp.content.decode('utf-8'), 'lxml')
            sections = bsoup.find_all('section', {'id': re.compile(r'section_(\d)+')})
            for sect in sections:
                section_text = sect.find('a', {'class': 'section-list-heading'}).get_text().strip()
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
                        "article_id": self.get_article_id(article.a['href'])
                    }
        else:
            print("Cannot get articles")

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
