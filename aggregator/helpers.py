import datetime
import json
import os
import sys
from dotenv import load_dotenv

import pymongo

chrome_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
load_dotenv()
testing = os.getenv('TESTING')


def get_db():
    if testing:
        client = pymongo.MongoClient(os.getenv('MONGO_URI'))
        return client['at-testing']
    else:
        client = pymongo.MongoClient(os.getenv('MONGO_URI'))
        return client['at']


def get_timestamp():
    return datetime.datetime.now().isoformat()


def get_max_id():
    max_id = int(get_db()['metadata'].find_one(
        {'name': 'max_id'})['value']) or 0
    return max_id


def get_next_id():
    max_id = get_max_id()
    next_id = max_id + 1
    get_db()['metadata'].update_one(
        {'name': 'max_id'}, {'$set': {'value': next_id}})
    return next_id


def get_stories():
    stories = list(get_db()['stories'].find({}).sort('published_at', -1))
    return stories


def save_stories(stories):
    get_db()['stories'].delete_many({})
    get_db()['stories'].insert_many(stories)


def get_groups():
    # groups is a list, convert to dict
    groups = {}
    for group in list(get_db()['groups'].find({})):
        groups[group['name']] = group['value']
    return groups


def save_groups(groups):
    groups_list = []
    for key in groups:
        group_stories = list(get_db()['stories'].find(
            {'id': {'$in': groups[key]}}))
        groups_list.append(
            {"name": key, "value": groups[key], "stories": group_stories})
        log(f"Saved group {key} with {len(group_stories)} stories")

    get_db()['groups'].delete_many({})
    get_db()['groups'].insert_many(groups_list)


def log(message):
    processed = message.replace("\n", " ")
    print(f'{get_timestamp()} {processed}', file=sys.stderr)

# get raw png bytes and convert to string
def get_image(url):
    import requests
    from io import BytesIO
    from PIL import Image
    response = requests.get(url, headers={'User-Agent': chrome_user_agent})
    image = Image.open(BytesIO(response.content))
    image = image.convert('RGB')
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


def get_hash(story):
    import hashlib
    # hash story["full_text"]
    return str(hashlib.sha256(story["full_text"].encode()))