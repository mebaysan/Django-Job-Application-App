.PHONY: help

help:
	@echo "Job Application Management Project"
	@echo "~~~~~~~~~~~~~~~"
	@echo ""
	@echo "check        : Health check"
	@echo "coverage     : Make test coverage"
	@echo "docup        : Run docker compose services"
	@echo "docdown      : Stop docker containers"
	@echo "migration    : Make django migrations"
	@echo "install      : Install python requirements"
	@echo "recover      : docdown + docup + wait + migrations + loaddata"
	@echo "runserver    : Run django server in debug mode"
	@echo "run_gunicorn : Run django server with gunicorn"
	@echo "static       : Collect static files"
	@echo "superuser    : Create django super user"
	@echo "test         : Start django test runner"
	@echo "translation  : Translation operation"
	@echo "wait         : Wait for 3 seconds"
	@echo ""

check:
	@python manage.py check

coverage:
	@coverage run --source='.' manage.py test
	@coverage report -m
	@coverage html
	@coverage xml

docup:
	@docker-compose up -d --build

docdown:
	@docker-compose down -v

dumpdata:
	@python manage.py dumpdata -o dummy.json

loaddata:
	@python manage.py loaddata scripts/dummy.json

migration:
	@python manage.py makemigrations
	@python manage.py migrate

install:
	@pip install -r requirements.txt

recover: install docdown docup wait migration loaddata
	@echo "\n\t~~~~~~~~~~~~~~~"
	@echo "\tusername: admin"
	@echo "\tpassword: 123"
	@echo "\t~~~~~~~~~~~~~~~\n"

recover_refactor: install docdown docup wait migration superuser
	@echo "\n\t~~~~~~~~~~~~~~~"
	@echo "\tusername: admin"
	@echo "\tpassword: 123"
	@echo "\t~~~~~~~~~~~~~~~\n"

runserver:
	@python manage.py runserver 127.0.0.1:8000

run_gunicorn:
	@gunicorn job_application_app.wsgi -b 0.0.0.0:8000

collect:
	@python manage.py collectstatic

superuser:
	@python manage.py createsuperuser

tests:
	@python manage.py test

translation:
	@python manage.py makemessages -l tr
	@python manage.py compilemessages

wait:
	@sleep 3

rundemo:
	@make collect 
	@make migration 
	@make loaddata 
	@make run_gunicorn