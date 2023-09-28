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
    client = pymongo.MongoClient(os.getenv('MONGO_URI'))
    return client['at']

def get_timestamp():
    return datetime.datetime.now().isoformat()

def get_max_id():
    max_id = 0
    if testing:
        max_id = int(open('db/max_id.txt').read())
    else:
        max_id = get_db()['metadata'].find_one({'name': 'max_id'})['value']
    return max_id
        
def get_next_id():
    max_id = get_max_id()
    next_id = max_id + 1
    if testing:
        open('db/max_id.txt', 'w').write(str(next_id))
    else:
        get_db()['metadata'].update_one({'name': 'max_id'}, {'$set': {'value': next_id}})
    return next_id

def get_stories():
    stories = []
    if testing:
        stories = json.loads(open('db/stories.json').read())
        stories.sort(key=lambda story: story['published_at'], reverse=True)
    else:
        stories = list(get_db()['stories'].find({}).sort('published_at', -1))
    return stories

def save_stories(stories):
    if testing:
        stories.sort(key=lambda story: story['published_at'], reverse=True)
        open('db/stories.json', 'w').write(json.dumps(stories))
    else:
        get_db()['stories'].delete_many({})
        get_db()['stories'].insert_many(stories)

def get_groups():
    groups = []
    if testing:
        groups = json.loads(open('db/groups.json').read())
    else:
        groups = list(get_db()['groups'].find({}))
    return groups

def save_groups(groups):
    if testing:
        open('db/groups.json', 'w').write(json.dumps(groups))
    else:
        get_db()['groups'].delete_many({})
        get_db()['groups'].insert_many(groups)

def log(message):
    processed = message.replace("\n", " ")
    print(f'{get_timestamp()} {processed}', file=sys.stderr)