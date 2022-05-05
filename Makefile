banco:
	docker run --rm --name db_sistemas_gestao -v ${PWD}/../.pg_sistemas_gestao:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres -p 5405:5432 -d postgres
lint:
	flake8 --count --exclude=*/migrations/*,*/fixtures/*,./sistema_gestao_projetos/*,manage.py;
test:
	./manage.py test -v2
