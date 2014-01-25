from datetime import timedelta

BROKER_URL = 'mongodb://localhost:27017/valar'

CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULE = {
    'once-a-minute': {
      'task': 'tasks.save_miner_stats',
      'schedule': timedelta(seconds=10),
    },
}
