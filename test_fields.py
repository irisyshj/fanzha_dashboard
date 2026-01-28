from services.feishu_client import FeishuClient
import json

client = FeishuClient()
records = client.get_all_records()

if records:
    r = records[0]
    fields = r.get('fields', {})

    print('Available field names:')
    for key in fields.keys():
        print(f'  "{key}"')

    print('\nTrying to find matching fields:')
    # 检查各种可能的字段名
    possible_names = ['标题', '标题', 'title', 'Title']
    for name in possible_names:
        if name in fields:
            print(f'  Found: "{name}" = {fields[name][:30]}...')

    date_names = ['日期', '日期', 'date', 'Date']
    for name in date_names:
        if name in fields:
            print(f'  Found: "{name}" = {fields[name]}')
