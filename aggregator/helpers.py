import datetime
import json
chrome_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"

def get_timestamp():
    return datetime.datetime.now().isoformat()

def get_max_id():
    max_id = int(open('db/max_id.txt').read())
    return max_id

def get_next_id():
    max_id = get_max_id()
    next_id = max_id + 1
    open('db/max_id.txt', 'w').write(str(next_id))
    return next_id

def get_stories():
    stories = json.loads(open('db/stories.json').read())
    stories.sort(key=lambda story: story['published_at'], reverse=True)
    return stories

def save_stories(stories):
    open('db/stories.json', 'w').write(json.dumps(stories))


def get_groups():
    groups = json.loads(open('db/groups.json').read())
    return groups

def save_groups(groups):
    open('db/groups.json', 'w').write(json.dumps(groups))

def log(message):
    print(f'{get_timestamp()} {message}')