from app import db

class Comment(db.EmbeddedDocument):
  id = db.IntField(unique=True, required=True)
  by = db.StringField(max_length=120, required=True)
  text = db.StringField(max_length=10000, required=True)
  parent = db.IntField(required=True)
  #todo missing the second level comments (kids)

  meta = {
      'indexes': ['cid']
  }

class Story(db.Document):
  sid = db.IntField(unique=True, required=True)
  by = db.StringField(max_length=120)
  text = db.StringField(max_length=10000)
  url = db.URLField(max_length=120)
  title = db.StringField(max_length=120, required=True)
  descendents = db.IntField()
  rank = db.IntField(required=True)
  #comments = db.ListField(db.EmbeddedDocumentField(Comment))

  meta = {
      'indexes': ['sid']
  }






