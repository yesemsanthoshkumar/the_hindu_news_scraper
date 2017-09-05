"""
Scraps the article and push it into the database
"""

from scraper import Scraper

import json
import sys
from datetime import datetime, timedelta
import re
import sys

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://localhost//27017')

db = client.scrap_test

req_dt = sys.argv[1].split("/")
scrapr = Scraper(req_dt)
print("Crawling hindu archive web for date", req_dt)
i = 0
for article in scrapr.get_articles():
    existing_duplicates = db['news'].find({'article_id' : article['article_id']}).count()
    if existing_duplicates == 0:
        article['_id'] = ObjectId()
        article['content'] = scrapr.get_document(article["url"])
        db['news'].insert(article)
