from app import celery, models
from app.tasks import fetch_stories

@celery.task
def update_stories():
  new_stories_rank = fetch_stories.get_top_stories_ids()

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
      story = fetch_stories.get_story(str(story_id))
      s = models.Story(
        sid=story['id'],
        rank=rank,
        title=story['title'],
        by=story['by']  
      )
      s.save()


  