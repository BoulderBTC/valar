from celery import Celery
from datetime import timedelta

app = Celery('tasks')
app.config_from_object('celeryconfig')

@app.task
def add(x, y):
  return x+y

