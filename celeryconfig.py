from celery.schedules import crontab

BROKER_URL = 'mongodb://localhost:27017/valar'

CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULE = {
    'once-a-minute': {
      'task': 'tasks.add',
      'schedule': crontab(minute='*/1'),
      'args': (16, 16)
    },
}
