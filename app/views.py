from flask import render_template, redirect, url_for, abort, make_response, jsonify, request
from app import app, db, models, constants, helpers
from app.tasks import other_tasks
import json

@app.errorhandler(400)
def not_found(error):
  return make_response(jsonify({"error": 'Bad request'}), 400)

@app.route('/')
def index():

  return render_template('index.html',
                          title='MultiLing-Hacker News',
                          stories=models.Story.objects(active=True).order_by('rank'))

@app.route('/unbabel_endpoint', methods=['POST'])
def add_translation():

  if not request.form or\
     not 'uid' in request.form or\
     len(request.form) > constants.UNBABEL_CALLBACK_MAX_LEN:
    abort(400)

  translation_object = request.form

  if translation_object['status'] == constants.STATUS_COMPLETED:
    uid = translation_object['uid']
    language = translation_object['target_language']
    text = translation_object['translated_text']
    other_tasks.activate_story.delay(uid, text, language)

  return jsonify(request.form), 201






