from flask import render_template, url_for
from app import app

@app.route('/')
#@app.route(url_for('index'))
def index():
  stories = [
    {
      'by': 'someone.com',
      'title': 'Cool stuff',
      'comments': [
        {
          'by': 'user1',
          'text': 'muito fixe!'
        },
        {
          'by': 'user2',
          'text': 'no gosto'
        }
      ]
    }
    ,
    {
      'by': 'anotherone.com',
      'title': 'More cool stuff',
      'comments': [
        {
          'by': 'user3',
          'text': 'ah pois' 
        }
      ]
    }
  ]
  return render_template('index.html',
                          title='MultiLing-Hacker News',
                          stories=stories)

