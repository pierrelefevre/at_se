import expressen_se
import llm
import helpers
import time
import db


def refresh():
    helpers.log('Refreshing stories')

    # scrape new stories
    new_stories = expressen_se.scrape()
    helpers.log(f'Scraped {len(new_stories)} stories')

    new = 0
    for new_story in new_stories:
        new_story['hash'] = helpers.get_hash(new_story)

        existing = db.get_story_by_url(new_story['url'])

        if existing and existing['hash'] == new_story['hash']:
            helpers.log(f'Skipped {new_story["title"]}')
            continue

        helpers.log(f'Added {new_story["title"]}')
        new_story['id'] = db.get_next_id()
        new_story['summary'] = llm.summarize(new_story)
        new_story['category'] = llm.pick_headline_topic(new_story['title'])

        try:
            image_url = llm.generate_image(new_story['title'])
            if image_url:
                new_story['image_url'] = image_url
                new_story['image_raw'] = helpers.get_image(
                    new_story['image_url'])
        except Exception as e:
            helpers.log(f'Failed to generate image: {e}', 'ERROR')

        if existing:
            db.replace_story(existing, new_story)
        else:
            db.insert_story(new_story)
        new += 1

    count = db.get_num_stories()

    helpers.log(f'Added {new} new stories, {count} total stories')
    return new


def group_headlines():
    helpers.log('Grouping headlines')
    headlines = db.get_headlines()
    grouped = llm.group_headlines(headlines)

    helpers.log(
        f'Grouped {len(headlines)} stories into {len(grouped.keys())} groups')

    db.save_groups(grouped)


def generate_digest():
    helpers.log('Generating digest')

    raw_headlines = db.get_headlines()
    headlines = []
    for headline in raw_headlines:
        headlines.append(headline['title'])

    db.save_digest(llm.generate_digest(headlines))


def verify():
    helpers.log('Verifying stories')

    missing_summaries = db.get_missing_summaries()
    for story in missing_summaries:
        if 'summary' not in story:
            story['summary'] = llm.summarize(story)
            db.replace_story(story, story)
            helpers.log(f'Fixed missing summary {story["title"]}')

    missing_categories = db.get_missing_categories()
    for story in missing_categories:
        if 'category' not in story:
            story['category'] = llm.pick_headline_topic(story['title'])
            db.replace_story(story, story)
            helpers.log(f'Fixed missing category {story["title"]}')

    missing_ids = db.get_missing_ids()
    for story in missing_ids:
        if 'id' not in story:
            story['id'] = helpers.get_next_id()
            helpers.log(f'Fixed missing ID {story["title"]}')
            db.replace_story(story, story)


def main():
    while True:
        helpers.log('Refreshing...')
        new = refresh()
        if new > 0:
            group_headlines()

        helpers.log('Sleeping for 10 minutes...')
        time.sleep(600)


if __name__ == '__main__':
    main()
