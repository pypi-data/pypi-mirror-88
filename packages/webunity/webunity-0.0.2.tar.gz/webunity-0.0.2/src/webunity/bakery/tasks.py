import os
import logging
from django.conf import settings
from django.core import management
from celery import Celery

from .exceptions import CMSError

logger = logging.getLogger('cms')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
app = Celery('webunity.bakery')
app.config_from_object(settings, namespace='CMS')
app.control.purge()
app.autodiscover_tasks()

INTERVAL_BUILD = 5


@app.task(bind=True, max_retries=3)
def build(self):
    try:
        management.call_command('build')
    except CMSError as exc:
        self.retry(exc=exc, countdown=INTERVAL_BUILD * self.request.retries)
