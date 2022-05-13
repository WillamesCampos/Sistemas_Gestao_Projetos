banco:
	docker stop db_sistemas_gestao || true;
	docker container rm db_sistemas_gestao || true;
	docker run  -d --rm --name db_sistemas_gestao -v ${PWD}/../.pg_sistemas_gestao:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres -p 5405:5432 -d postgres
lint:
	flake8 --count --exclude=*/migrations/*,*/fixtures/*,./sistema_gestao_projetos/*,manage.py;
test:
	./manage.py test -v2
celery:
	docker stop redis || true;
	docker container rm redis || true;
	docker run -d --rm --name redis -p 6379:6379 redis;
	rm celerybeat.pid || true;
	celery -A sistema_gestao_projetos.celerybeat-schedule beat --detach;
	celery -A sistema_gestao_projetos worker -l INFO;