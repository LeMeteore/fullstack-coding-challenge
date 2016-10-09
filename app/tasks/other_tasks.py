import requests
from app import celery, models, constants, helpers
import config

@celery.task
def get_story(sid, rank):
  ''' fetches story by sid, request its translation and stores it in DB 

      sid: int
      rank: int'''

  s = helpers.get_hn_story(str(sid))

  story = models.Story(
    sid=sid,
    rank=rank,
    title=s['title'],
    pt_title="",
    fr_title="",
    active=False
  )

  helpers.translate_story_request(sid, story.title)

  # delete stories if they exist in this position
  models.Story.objects(rank=rank, active=False).delete()

  story.save()

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
    misplaced_story.save()

  s.save()

@celery.task
def activate_story(uid, text, language):
  ''' Sets the translation of the story and updates story to active '''
  try:
    sid = helpers.uid_to_sid(uid)
  except ValueError:
    return

  story = models.Story.objects(sid=sid).first()

  if language == constants.PORTUGUESE:
    story.pt_title = text
  elif language == constants.FRENCH:
    story.fr_title = text
  story.active = True

  # delete previous story in this rank
  models.Story.objects(rank=story.rank, active=True).delete()

  story.save()

