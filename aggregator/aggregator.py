import expressen_se
import llm
import helpers


def refresh():
    # Get current stories
    stories = helpers.get_stories()

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


def group_headlines():
    stories = helpers.get_stories()

    headlines = []
    for story in stories:
        headlines.append({'id': story['id'], 'title': story['title']})
    grouped = llm.group_headlines(headlines)

    helpers.log(f'Grouped {len(stories)} into {len(grouped)} groups')

    helpers.save_groups(grouped)


def main():
    refresh()
    group_headlines()


if __name__ == '__main__':
    main()
