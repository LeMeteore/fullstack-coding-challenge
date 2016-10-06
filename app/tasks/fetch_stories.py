import requests
from app import celery, models
import random

API_URL = "https://hacker-news.firebaseio.com/v0/"
ITEM_ENDPOINT = "item/"
TOP_STORIES_ENDPOINT = "topstories/"
JSON_FORMAT = ".json"

def get_top_stories_ids(n=10, api_url=API_URL, endpoint=TOP_STORIES_ENDPOINT, resp_format=JSON_FORMAT):
  url = api_url+endpoint+resp_format
  #todo: check status and exceptions
  stories_ids = requests.get(url).json()[:n]
  
  stories_rank = {}
  for i, sid in enumerate(stories_ids):
    stories_rank[sid] = i

  return stories_rank
  
def get_story(sid, api_url=API_URL, endpoint=ITEM_ENDPOINT, resp_format=JSON_FORMAT):
  url = api_url+endpoint+sid+resp_format
  payload = {'id': sid}
  r = requests.get("https://hacker-news.firebaseio.com/v0/item", params=payload)
  #todo: check status and exceptions
  return requests.get(url).json()

