from app import celery, models, helpers
from app.tasks import other_tasks

@celery.task
def update_stories():
  new_stories_rank = helpers.get_top_stories_ids()

  already_present = set()
  for old_story in models.Story.objects:
    if old_story.sid in new_stories_rank:
      already_present.add(old_story.sid)
      old_story.rank = new_stories_rank[old_story.sid]
      old_story.save()
    else:
      old_story.delete()

  for story_id, rank in new_stories_rank.iteritems():
    if story_id not in already_present:
      other_tasks.get_story.delay(str(story_id), rank)

  