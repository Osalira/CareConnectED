# backend/backend/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# Namespace 'CELERY_' means all Celery-related config keys
# should be prefixed with 'CELERY_' in Django settings.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 
app.conf.update(
    broker_connection_retry_on_startup=True,
)
# for development
app.conf.worker_pool = 'solo'

#in production
# app.conf.worker_pool = 'prefork'  # Default pool for production

# Autodiscover tasks in all installed apps.
app.autodiscover_tasks()

broker_connection_retry_on_startup = True

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
