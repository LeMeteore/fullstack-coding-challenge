import requests

ITEM_ENDPOINT = "https://hacker-news.firebaseio.com/v0/item/"
TOP_STORIES_ENDPOINT = "https://hacker-news.firebaseio.com/v0/topstories.json"

class FetchStoriesJob():

  def run(self):
    top_ids = self._get_top_ten_stories_ids()
    
    top_stories = {}

    for i, story_id in enumerate(top_ids):
        story = self._get_story(str(story_id))
        story['rank']=i+1
        top_stories[story_id] = story
    
    return top_stories

  # --- private methods

  def _get_top_ten_stories_ids(self):
    url = TOP_STORIES_ENDPOINT
    #todo: check status and exceptions
    return requests.get(url).json()[:10]

  def _get_story(self, id):
    url = ITEM_ENDPOINT+id+'.json'
    r = requests.get(url)
    #todo: check status and exceptions
    return r.json()


