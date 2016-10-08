from app import constants
import requests

def make_hn_api_url(endpoint, sid=""):
  return constants.API_URL+endpoint+sid+constants.JSON_FORMAT

def get_top_stories_ids(n=10):
  url = make_hn_api_url(constants.TOP_STORIES_ENDPOINT)
  #todo: check status and exceptions
  stories_ids = requests.get(url).json()[:n]
  
  stories_rank = {}
  for i, sid in enumerate(stories_ids):
    stories_rank[sid] = i

  return stories_rank
