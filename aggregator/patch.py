import helpers
import llm

stories = helpers.get_stories()


for i, story in enumerate(stories):
    story['category'] = llm.pick_headline_topic(story['title'])
    helpers.log(f'{i}/{len(stories)}')

helpers.save_stories(stories)
