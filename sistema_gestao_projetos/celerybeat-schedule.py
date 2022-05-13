from .celery import app
from celery.schedules import crontab


# app.conf.beat_schedule = {
#     'invalida_licecas': {
#         'task': 'jogos.tasks.invalida_licecas',
#         'schedule': crontab(minute=0, hour=0)
#     }
# }
