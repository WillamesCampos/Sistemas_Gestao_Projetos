web: gunicorn sistema_gestao_projetos.wsgi --log-file -
heroku ps:scale worker=1
celery: celery -A sistema_gestao_projetos worker --pool=solo -l INFO
celery -A sistema_gestao_projetos.celerybeat-schedule beat --detach