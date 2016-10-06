from datetime import timedelta
from app import tasks

MONGODB_SETTINGS = {
  'db': 'multilingual_hacker_news',
  'username': '',
  'password': ''
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'




