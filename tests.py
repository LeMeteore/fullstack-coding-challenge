#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" tests """

import os
import unittest
from mongoengine import connect
from app import app
from flask_mongoengine import MongoEngine

from app.models import Story, Comment

from app import celery
from app.tasks.scheduled_tasks import update_stories

class TestCase(unittest.TestCase):
    def setUp(self):
        celery.conf.update(CELERY_ALWAYS_EAGER=True)
        self.app = app.test_client()

    def tearDown(self):
        Story.drop_collection()

    def test_update_stories(self):
        self.assertTrue(update_stories.delay())

    def test_create_story(self):
        comment = Comment(
            cid=1,
            by="foo",
            text="bar",
            parent=2,
            kids=[1, 2, 3],
        )

        story = Story(
            sid=1,
            rank=2,
            by="foo",
            title="bar",
            pt_uid="3",
            fr_uid="4",
            descendents=7,
            comments=[comment,]
        )
        story.save()
        assert Story.objects.count() == 1
        assert Story.objects.first().sid == 1

    def test_home_page(self):
        response = self.app.get('/')
        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main()

