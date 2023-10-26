import pymongo
import json
import os
import helpers

testing = os.getenv('TESTING')


def get_db():
    if testing:
        client = pymongo.MongoClient(os.getenv('MONGO_URI'))
        return client['at-testing']
    else:
        client = pymongo.MongoClient(os.getenv('MONGO_URI'))
        return client['at']


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


def get_story_by_id(id):
    story = get_db()['stories'].find_one({'id': id})
    return story


def get_story_by_url(url):
    story = get_db()['stories'].find_one({'url': url})
    return story


def replace_story(old, new):
    new['id'] = old['id']
    get_db()['stories'].replace_one({'id': old['id']}, new)
    return new


def insert_story(story):
    get_db()['stories'].insert_one(story)
    return story


def get_num_stories():
    return get_db()['stories'].count_documents({})


def get_latest_stories():
    return list(get_db()['stories'].find({}).sort('published_at', -1).limit(30))


def get_headlines():
    stories = get_latest_stories()
    headlines = []
    for story in stories:
        headlines.append({'id': story['id'], 'title': story['title']})
    return headlines


def get_digest():
    get_db()['digest'].find_one({})


def save_digest(digest):
    get_db()['digest'].delete_many({})
    get_db()['digest'].insert_one({"digest": digest})


def get_groups():
    return list(get_db()['groups'].find({}))


def save_groups(groups):
    groups_list = []
    for key in groups:
        group_stories = list(get_db()['stories'].find(
            {'id': {'$in': groups[key]}}))
        groups_list.append(
            {"name": key, "value": groups[key], "stories": group_stories})
        helpers.log(f"Saved group {key} with {len(group_stories)} stories")

    get_db()['groups'].delete_many({})
    get_db()['groups'].insert_many(groups_list)


def get_missing_summaries():
    return list(get_db()['stories'].find({'summary': {'$exists': False}}))


def get_missing_categories():
    return list(get_db()['stories'].find({'category': {'$exists': False}}))


def get_missing_ids():
    return list(get_db()['stories'].find({'id': {'$exists': False}}))
