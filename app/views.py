from flask import render_template, redirect, url_for, abort, make_response, jsonify, request
from app import app, db, models, constants, helpers
from app.tasks import other_tasks
import json
from celery import group

@app.errorhandler(400)
def not_found(error):
  return make_response(jsonify({"error": 'Bad request'}), 400)

@app.route('/')
def index():

  return render_template('index.html',
                          title='MultiLing-Hacker News',
                          stories=models.Story.objects.order_by('rank'))

@app.route('/unbabel_endpoint', methods=['POST'])
def add_translation():

  if not request.form or\
     not 'uid' in request.form or\
     len(request.form) > constants.UNBABEL_CALLBACK_MAX_LEN:
    abort(400)

  translation_object = request.form

  if translation_object['status'] == constants.STATUS_COMPLETED:
    uid = translation_object['uid']
    text = translation_object['translated_text']
    other_tasks.update_story_translation.delay(uid, text)

  elif translation_object['status'] in constants.FAILED_STATUSES:
    text = translation_object['translated_text']
    uid = translation_object['uid']
    retry_translation.delay(uid, text)

  return jsonify(request.form), 201

@app.route('/status')
def translation_status():

  new = other_tasks.get_translations_status.s(constants.STATUS_NEW)
  progress = other_tasks.get_translations_status.s(constants.STATUS_TRANSLATING)

  g = group(new, progress)().get()
  
  all_status = []
  for status_group in g:
    this_status = []
    for translation_request in status_group['objects']:
      single_request = {'target_language': translation_request['target_language']} 

      sid = helpers.get_sid_from_uid(translation_request['uid'])
      text = models.Story.objects(sid=sid).only('title').first().title
      single_request['text'] = text

      this_status.append(single_request)

    all_status.append(this_status)

  completed = []
  for s in models.Story.objects(pt_title__exists=True, fr_title__exists=True):
    fr_request = {'target_language': constants.FRENCH, 'text': s.title, 'result': s.fr_title}
    pt_request = {'target_language': constants.PORTUGUESE, 'text': s.title, 'result': s.pt_title}
    completed += [fr_request, pt_request]

  return render_template('status.html',
                         title='Translations Status',
                         new=all_status[0],
                         translating=all_status[1],
                         completed=completed)




