import requests
from app import celery, models, constants, helpers

@celery.task  
def get_story(sid, rank):
  ''' Fetches and saves in DB the hacker news story with id sid.''' 
  url = helpers.make_hn_api_url(constants.ITEM_ENDPOINT, sid=sid)

  r = requests.get(url)
  print r.status_code
  print r.url
  story = r.json()
  #todo: check status and exceptions

  print story
  s = models.Story(
    sid=story['id'],
    rank=rank,
    title=story['title'],
    by=story['by']  
  )
  s.save()

