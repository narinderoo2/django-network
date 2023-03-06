
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "customeUser.settings")
app = Celery("customeUser")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

celery = Celery(__name__)
celery.config_from_object(__name__)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    
    
app.conf.beat_schedule = {
    'multiply-every-5-seconds': {
        'task': 'multiply_two_numbers',
        'schedule': 30.0,
        'args': (16, 16)
    },
    'save_device_details': {
        'task': 'device_details_save',
        'schedule': 60.0,
    },
    
}     
