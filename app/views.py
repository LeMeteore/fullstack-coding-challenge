from flask import render_template, redirect, url_for
from app import app, db, models, celery
import time, random

from app.tasks import fetch_stories

@app.route('/')
def index():

  return render_template('index.html',
                          title='MultiLing-Hacker News',
                          stories=models.Story.objects.order_by('rank'))

