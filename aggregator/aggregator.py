import expressen_se
import llm
import helpers
import time


def refresh():
    # Get current stories
    stories = helpers.get_stories()

    stories = verify(stories)

    # scrape new stories
    new_stories = expressen_se.scrape()
    helpers.log(f'Scraped {len(new_stories)} stories')

    new = 0
    for new_story in new_stories:
        if not any(story['title'] == new_story['title'] for story in stories):
            helpers.log(f'Added {new_story["title"]}')
            new_story['id'] = helpers.get_next_id()
            new_story['summary'] = llm.summarize(new_story)
            new_story['category'] = llm.pick_headline_topic(new_story['title'])
            stories.append(new_story)
            new += 1
            helpers.save_stories(stories)
        else:
            helpers.log(f'Skipped {new_story["title"]}')

    helpers.log(f'Added {new} new stories, {len(stories)} total stories')


def verify(stories):
    for story in stories:
        if 'summary' not in story:
            story['summary'] = llm.summarize(story)
            helpers.log(f'Fixed missing summary {story["title"]}')
            helpers.save_stories(stories)

        if 'category' not in story:
            story['category'] = llm.pick_headline_topic(story['title'])
            helpers.log(f'Fixed missing category {story["title"]}')
            helpers.save_stories(stories)

        if 'id' not in story:
            story['id'] = helpers.get_next_id()
            helpers.log(f'Fixed missing ID {story["title"]}')
            helpers.save_stories(stories)

    return stories


def group_headlines():
    stories = helpers.get_stories()

    headlines = []
    for story in stories:
        headlines.append({'id': story['id'], 'title': story['title']})
    grouped = llm.group_headlines(headlines)

    helpers.log(f'Grouped {len(stories)} into {len(grouped.keys())} groups')

    helpers.save_groups(grouped)


def main():
    while True:
        helpers.log('Refreshing...')
        refresh()
        group_headlines()
        helpers.log('Sleeping for 10 minutes...')
        time.sleep(600)


if __name__ == '__main__':
    main()
