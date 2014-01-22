from celery.schedules import crontab

BROKER_URL = 'mongodb://localhost:27017/valar'

CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULE = {
    'once-a-minute': {
      'task': 'tasks.save_miner_stats',
      'schedule': crontab(minute='*/1')
    },
}
