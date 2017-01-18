#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Application configuration"""

from datetime import timedelta
from app import tasks

MONGODB_SETTINGS = {
    'db': 'multilingual_hacker_news',
    'username': '',
    'password': ''
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_IMPORTS = ('app.tasks.scheduled_tasks', )
CELERYBEAT_SCHEDULE = {
    'add-every-10-minutes': {
        'task': 'app.tasks.scheduled_tasks.update_stories',
        'schedule': timedelta(minutes=2),
    },
}

UNBABEL_USERNAME = "ndkpatt"
UNBABEL_KEY = "3ab3f760fbad437fbb582b98a3c3a1bc58d43769"
UNBABEL_EMAIL = "ndkpatt@gmail.com"




