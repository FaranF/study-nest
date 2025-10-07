from calendar import c
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'study_nest.settings')
celery = Celery('study_nest')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()

# uncommand __init__ and run:
# celery -A study_nest worker --loglevel=info

# pipenv install flower
# celery -A study_nest flower # optional: --port=5555