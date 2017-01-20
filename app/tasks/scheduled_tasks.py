#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Celery scheduled tasks """

from app import celery, models, helpers
from app.tasks import other_tasks
from celery import group


@celery.task
def update_stories():
    """ Function to update stories """
    new_stories_rank = helpers.get_top_stories_ids()

    for story_id, rank in new_stories_rank.items():
        story = models.Story.objects(sid=story_id).first()

        if story:
            #store the story in new rank
            other_tasks.swap_stories_by_rank.delay(story.to_json(), rank)

        else:
            # get story and translate it
            other_tasks.get_story.delay(story_id, rank)

