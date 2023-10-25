import expressen_se
import llm
import helpers
import time


def refresh():
    helpers.log('Refreshing stories')
    # Get current stories
    stories = helpers.get_stories()

    stories = verify(stories)

    # scrape new stories
    new_stories = expressen_se.scrape()
    helpers.log(f'Scraped {len(new_stories)} stories')

    new = 0
    for new_story in new_stories:
        new_story['hash'] = helpers.get_hash(new_story)
        if not any(story['hash'] == new_story["hash"] for story in stories):
            helpers.log(f'Added {new_story["title"]}')
            new_story['id'] = helpers.get_next_id()
            new_story['summary'] = llm.summarize(new_story)
            new_story['category'] = llm.pick_headline_topic(new_story['title'])
            # images are disabled for now
            # new_story['image_url'] = llm.generate_image(new_story['title'])
            # new_story['image_raw'] = helpers.get_image(new_story['image_url'])
            stories.append(new_story)
            new += 1
        else:
            helpers.log(f'Skipped {new_story["title"]}')

    helpers.log(f'Added {new} new stories, {len(stories)} total stories')
    helpers.save_stories(stories)
    return new


def verify(stories):
    helpers.log('Verifying stories')
    for story in stories:
        if 'summary' not in story:
            story['summary'] = llm.summarize(story)
            helpers.log(f'Fixed missing summary {story["title"]}')

        if 'category' not in story:
            story['category'] = llm.pick_headline_topic(story['title'])
            helpers.log(f'Fixed missing category {story["title"]}')

        if 'id' not in story:
            story['id'] = helpers.get_next_id()
            helpers.log(f'Fixed missing ID {story["title"]}')

        if 'hash' not in story:
            story['hash'] = helpers.get_hash(story)
            helpers.log(f'Fixed missing hash {story["title"]}')

    return stories


def group_headlines():
    helpers.log('Grouping headlines')
    stories = helpers.get_stories()

    headlines = []
    for story in stories:
        headlines.append({'id': story['id'], 'title': story['title']})
    grouped = llm.group_headlines(headlines)

    helpers.log(
        f'Grouped {len(stories)} stories into {len(grouped.keys())} groups')

    helpers.save_groups(grouped)


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
