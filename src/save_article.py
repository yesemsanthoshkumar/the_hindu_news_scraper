"""
Scraps the article and push it into the database
"""

import sys
from datetime import date

import argparse
from bson.objectid import ObjectId
from pymongo import MongoClient

from scraper import Scraper

client = MongoClient('mongodb://localhost//27017')

db = client.scrap_test

arguments = argparse.ArgumentParser(
    description="Scraps the news document from the hindu archives"
)
arguments.add_argument(
    '--start-date',
    dest='start_date',
    default=date.today().strftime("%Y/%m/%d"),
    help="Start date of crawling"
)
arguments.add_argument(
    '--end-date',
    dest='end_date',
    default=date.today().strftime("%Y/%m/%d"),
    help="End date of crawling"
)
args = arguments.parse_args()

scrapr = Scraper(args.start_date, args.end_date)

for article in scrapr.get_articles():
    existing_duplicates = db['news'].find({'article_id' : article['article_id']}).count()
    if existing_duplicates == 0:
        article['_id'] = ObjectId()
        article['content'] = scrapr.get_document(article["url"])
        db['news'].insert(article)
        print("Inserted article", article["article_id"], "from date", article['article_date'])
    else:
        print("Record already found..", article['article_id'])
