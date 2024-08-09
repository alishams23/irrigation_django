
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')


app.conf.task_queues = {
    'default': {
        'exchange': 'default',
        'exchange_type': 'direct',
        'binding_key': 'default',
    },
    'sms_queue': {
        'exchange': 'sms_queue',
        'exchange_type': 'direct',
        'binding_key': 'sms_queue',
    }
}

app.conf.task_routes = {
    'main.tasks.check_time_field': {'queue': 'default'},
    'main.tasks.sendSms': {'queue': 'sms_queue'},
}

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.broker_connection_retry_on_startup = True