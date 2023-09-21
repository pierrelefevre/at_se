import expressen_se
# import aftonbladet_se
# import svt_se
import sys
import os
import time
import datetime
import json
import requests

def main():
    stories = []
    stories.extend(json.loads(open('test.json').read()))
    # stories.extend(expressen_se.scrape())
    # stories.extend(aftonbladet_se.scrape())
    # stories.extend(svt_se.scrape())
    print(len(stories))

    # Write to file
    with open('data.json', 'w') as outfile:
        json.dump(stories, outfile)



if __name__ == '__main__':
    main()