web: gunicorn sistema_gestao_projetos.wsgi --log-file -

celery: celery -A sistema_gestao_projetos worker --pool=solo -l INFO