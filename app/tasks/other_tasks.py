#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from app import celery, models, constants, helpers
import config
from celery import group

@celery.task
def get_story(sid, rank):
    ''' fetches story by sid, request its translation and stores it in DB
        sid: int
        rank: int'''

    s = helpers.get_hn_story(str(sid))

    pt_uid = helpers.construct_uid(sid, constants.PORTUGUESE)
    fr_uid = helpers.construct_uid(sid, constants.FRENCH)
    request_translations.delay(s['title'], [pt_uid, fr_uid])

    story = models.Story(
        sid=sid,
        rank=rank,
        by=s['by'],
        title=s['title'],
        pt_uid=pt_uid,
        fr_uid=fr_uid,
        descendents=s['descendants']
    )

    # delete stories if they exist in this position
    models.Story.objects(rank=rank).delete()
    story.insert_one()

    # get comments
    print( "#"*100)
    for cid in s['kids']:
        print( "CID: ", cid)
        get_hn_comment.delay(sid, cid)
    print( "-"*100)


@celery.task
def get_hn_comment(sid, cid):
    url = helpers.make_hn_api_url(constants.HN_ITEM_ENDPOINT, item_id=str(cid))
    r = requests.get(url)
    #todo: check for errors
    item = r.json()

    if 'text' in item and 'by' in item:
        # save comment in DB
        comment = models.Comment(
            cid=cid,
            by=item['by'] if 'by' in item else "",
            text=item['text'],
            parent=sid
        )

        models.Story.objects(sid=sid).update_one(push__comments=comment)

@celery.task
def swap_stories_by_rank(s, new_rank):
    previous_rank = s.rank

    if previous_rank == new_rank:
        return

    # todo: in this query specify that acitve must be True
    misplaced_story = models.Story.objects(rank=new_rank).first()
    s.rank = new_rank

    if misplaced_story:
        misplaced_story.rank = previous_rank
        misplaced_story.insert_one()

    s.insert_one()

@celery.task
def request_translations(text, uids):
    headers = helpers.get_unbabel_api_headers()
    url = constants.UNBABEL_URL + constants.TRANSLATE_ENDPOINT

    payload = {
        "text": text,
        "source_language": constants.ENGLISH,
        "text_format": "text",
        "callback_url": "http://e5d89c49.ngrok.io/unbabel_endpoint"
        }
    for uid in uids:
        payload['target_language'] = helpers.get_language_from_uid(uid)
        payload['uid'] = uid

        r = requests.post(url, json=payload, headers=headers)

@celery.task
def update_story_translation(uid, text):
    ''' Sets the translation of the story and updates story to active '''
    try:
        sid = helpers.get_sid_from_uid(uid)
        language = helpers.get_language_from_uid(uid)
    except ValueError:
        return

    story = models.Story.objects(sid=sid).first()

    if language == constants.PORTUGUESE:
        story.pt_title = text
    elif language == constants.FRENCH:
        story.fr_title = text

    story.insert_one()

@celery.task
def retry_translation(uid, text):
    sid = helpers.get_sid_from_uid(uid)
    language = helpers.get_language_from_uid(uid)

    new_uid = helpers.construct_uid(sid, language)
    story = models.Story.objects(sid=sid).first()

    if language == constants.PORTUGUESE:
        story.pt_uid = new_uid
    elif language == constants.FRENCH:
        story.fr_uid = new_uid

    request_translations.delay(text, [new_uid])

@celery.task
def get_translations_status(status=None):
    headers = helpers.get_unbabel_api_headers()
    url = constants.UNBABEL_URL + constants.TRANSLATE_ENDPOINT
    if status:
        payload = {"status": status}

    r = requests.get(url, params=payload, headers=headers)
    return r.json()
