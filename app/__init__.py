#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Init app module """

from flask import Flask
from celery import Celery

from flask_mongoengine import MongoEngine
import config



app = Flask(__name__)
app.config.from_object('config')
app.config.from_envvar('TEST_SETTINGS',silent=True)

celery = Celery(app.name, broker=config.CELERY_BROKER_URL)
celery.conf.update(app.config)

db = MongoEngine(app)
from app import views
