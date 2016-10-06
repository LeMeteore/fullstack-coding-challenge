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
    'add-every-1-minutes': {
        'task': 'app.tasks.scheduled_tasks.update_stories',
        'schedule': timedelta(minutes=1),
    },
}




