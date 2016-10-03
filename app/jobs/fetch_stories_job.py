import requests

ITEM_ENDPOINT = "https://hacker-news.firebaseio.com/v0/item/"
TOP_STORIES_ENDPOINT = "https://hacker-news.firebaseio.com/v0/topstories.json"

class FetchStoriesJob():

  def run(self):
    top_ids = self._get_top_ten_stories_ids()
    
    top_stories = []
    for story_id in top_ids:
        story = self._get_story(str(story_id))
        top_stories.append(story)
    
    return top_stories

  # --- private methods

  def _get_top_ten_stories_ids(self):
    url = TOP_STORIES_ENDPOINT
    #todo: check status
    return requests.get(url).json()[:10]

  def _get_story(self, id):
    url = ITEM_ENDPOINT+id+'.json'
    print url
    r = requests.get(url)
    return r.json()


