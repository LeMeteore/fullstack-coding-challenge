#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import constants
import requests, config, time

def make_hn_api_url(endpoint, item_id=""):
    return constants.HN_URL+endpoint+item_id+constants.HN_JSON_FORMAT

def get_top_stories_ids(n=10):
    url = make_hn_api_url(constants.HN_TOP_STORIES_ENDPOINT)
    #todo: check status and exceptions
    try:
        stories_ids = requests.get(url).json()[:n]
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    stories_rank = {}
    for i, sid in enumerate(stories_ids):
        stories_rank[int(sid)] = i

    return stories_rank

def get_hn_story(sid):
    ''' sid: str '''
    url = make_hn_api_url(constants.HN_ITEM_ENDPOINT, item_id=sid)
    print(url)
    try:
        r = requests.get(url)
    # except Exception:
    #     _, err, _ = sys.exc_info()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    story = r.json()
    #todo: check status and exceptions

    return story

def get_unbabel_api_headers():
    key = f'ApiKey {config.UNBABEL_USERNAME}:{config.UNBABEL_KEY}'
    return {'Authorization': key}

def construct_uid(sid, language):
    to_epoch = int(time.time())
    return '{language}:{sid}:{to_epoch}'

def get_sid_from_uid(uid):
    return int(uid.split(':')[1])

def get_language_from_uid(uid):
    return uid.split(':')[0]
