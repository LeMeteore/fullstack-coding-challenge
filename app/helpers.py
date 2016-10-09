from app import constants
import requests, config, time

def make_hn_api_url(endpoint, sid=""):
  return constants.HN_URL+endpoint+sid+constants.HN_JSON_FORMAT

def get_top_stories_ids(n=10):
  url = make_hn_api_url(constants.HN_TOP_STORIES_ENDPOINT)
  #todo: check status and exceptions
  stories_ids = requests.get(url).json()[:n]

  stories_rank = {}
  for i, sid in enumerate(stories_ids):
    stories_rank[int(sid)] = i

  return stories_rank

def get_hn_story(sid):
  ''' sid: str '''
  url = make_hn_api_url(constants.HN_ITEM_ENDPOINT, sid=sid)
  r = requests.get(url)
  story = r.json()
  #todo: check status and exceptions

  return story

def translate_story_request(sid, title):

  key = 'ApiKey {}:{}'.format(config.UNBABEL_USERNAME, config.UNBABEL_KEY)
  headers = {'Authorization': key}
  url = constants.UNBABEL_URL + constants.TRANSLATE_ENDPOINT

  payload = {
    "text": title,
    "target_language": constants.PORTUGUESE,
    "source_language": constants.ENGLISH,
    "text_format": "text",
    "uid": sid_to_uid(sid),
    "callback_url": "http://e5d89c49.ngrok.io/unbabel_endpoint"
  }

  r = requests.post(url, json=payload, headers=headers)
  
def sid_to_uid(sid):
  sec_to_epoch = int(time.time())
  return '{}:{}'.format(sid, sec_to_epoch)

def uid_to_sid(uid):
  return int(uid.split(':')[0])

