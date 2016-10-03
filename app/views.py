from flask import render_template, url_for
from app import app

from app.jobs import fetch_stories_job

@app.route('/')
#@app.route(url_for('index'))
def index():
  
  stories = fetch_stories_job.FetchStoriesJob().run()
  return render_template('index.html',
                          title='MultiLing-Hacker News',
                          stories=stories)

