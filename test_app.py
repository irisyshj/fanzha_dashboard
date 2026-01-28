import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from services.cache import get_all_articles

with app.app_context():
    articles = get_all_articles()
    print(f'Total articles: {len(articles)}')

    if articles:
        print('\nFirst article:')
        print(f'  ID: {articles[0].id}')
        print(f'  Title: {articles[0].title}')
        print(f'  Date: {articles[0].date}')
        print(f'  Summary: {articles[0].summary[:50] if articles[0].summary else None}...')
        print(f'  Source: {articles[0].source}')
    else:
        print('No articles found!')
