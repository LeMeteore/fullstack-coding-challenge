from datetime import timedelta
from app import tasks

MONGODB_SETTINGS = {
  'db': 'multilingual_hacker_news',
  'username': '',
  'password': ''
}

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_IMPORTS = ('app.tasks.scheduled_tasks', )
CELERYBEAT_SCHEDULE = {
    'add-every-10-minutes': {
        'task': 'app.tasks.scheduled_tasks.update_stories',
        'schedule': timedelta(minutes=2),
    },
}

UNBABEL_USERNAME = "pixels.camp.508"
UNBABEL_KEY = "efce0e40d04fadb0dd8291855dc18007c674b105"
UNBABEL_EMAIl = "pixels.camp.508@unbabel.com"



