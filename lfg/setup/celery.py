from celery import Celery
import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
