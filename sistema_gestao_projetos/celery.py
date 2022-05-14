from __future__ import absolute_import
import os
from celery import Celery
from decouple import config


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    f'sistema_gestao_projetos.settings.{config("ENV", "production")}'
)

app = Celery('sistema_gestao_projetos')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
