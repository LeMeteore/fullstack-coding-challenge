from flask import render_template, url_for
from app import app, db, models

from app.jobs import fetch_stories_job

@app.route('/')
def index():
  
  stories = fetch_stories_job.FetchStoriesJob().run()

  # delete previous top stories
  for story in models.Story.objects:
    if story.sid not in stories:
      story.delete()

  for i, (story_id, story) in enumerate(stories.iteritems()):
    prev_story = models.Story.objects(sid=story['id'])

    if prev_story:
      #todo: add new comments
      prev_story.rank=story['rank']

    else:
      s = models.Story(
          sid=story['id'],
          rank=story['rank'],
          title=story['title'],
          by=story['by']  
      )

      s.save()

  return render_template('index.html',
                          title='MultiLing-Hacker News',
                          stories=models.Story.objects.order_by('rank'))

