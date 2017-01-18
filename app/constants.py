#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Hacker News
HN_URL = "https://hacker-news.firebaseio.com/v0/"
HN_ITEM_ENDPOINT = "item/"
HN_TOP_STORIES_ENDPOINT = "topstories/"
HN_JSON_FORMAT = ".json"

# Unbabel
UNBABEL_URL = "https://sandbox.unbabel.com/tapi/v2/"
TRANSLATE_ENDPOINT = "translation/"
UNBABEL_CALLBACK_MAX_LEN = 10
STATUS_COMPLETED = "completed"
STATUS_FAILED = "failed"
STATUS_TRANSLATING = "translating"
STATUS_NEW = "new"
STATUS_CANCELED = "canceled"
FAILED_STATUSES = [STATUS_FAILED, STATUS_CANCELED]

PORTUGUESE = "pt"
FRENCH = "fr"
ENGLISH = "en"
