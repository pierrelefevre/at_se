import datetime
import sys
from dotenv import load_dotenv
import hashlib

chrome_user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
load_dotenv()


def get_timestamp():
    return datetime.datetime.now().isoformat()


def log(message, level="INFO"):
    processed = message.replace("\n", " ")
    print(f'[{level}] {get_timestamp()} {processed}', file=sys.stderr)

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
    return str(hashlib.sha256(story["full_text"].encode()))
