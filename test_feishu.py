from services.feishu_client import FeishuClient
from config import Config
import json

client = FeishuClient()
records = client.get_all_records()

print('Total records:', len(records))

if records:
    r = records[0]
    print('\nFirst record fields:')
    print(json.dumps(r.get('fields', {}), ensure_ascii=False, indent=2))

    print('\nField mapping:')
    print(Config.FIELD_MAPPING)

    # 测试转换
    from models.article import Article
    article = Article.from_feishu_record(r, Config.FIELD_MAPPING)
    print('\nConverted article:')
    print(f'  ID: {article.id}')
    print(f'  Title: {article.title}')
    print(f'  Date: {article.date}')
    print(f'  Summary: {article.summary[:50] if article.summary else None}...')
    print(f'  Source: {article.source}')
