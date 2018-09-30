index:
		./manage.py search_index --models borme.Company --populate
		./manage.py search_index --models borme.Person --populate

reindex:
		./manage.py search_index --delete
		# the index must be created outside Django
		./manage.py search_index --models borme.Company --populate
		./manage.py search_index --models borme.Person --populate

robotstxt:
		./manage.py regenerate_robotstxt

backups:
		s3cmd ls s3://libreborme-prod/backups/database/

recreate_db:
		./manage.py reset_db --noinput
		./manage.py migrate
		./manage.py loaddata ./libreborme/fixtures/config.json
		./manage.py loaddata ./alertas/fixtures/alertasconfig.json
		# ./manage.py createsuperuser --username admin --email pablo@anche.no
		./manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'pablo@anche.no', '000000')"
		./manage.py djstripe_sync_customers
		./manage.py djstripe_sync_plans_from_stripe


recreate_db2:
		# pg_dump -c -C -h localhost -U libreborme > clean_dump.sql
		# no va
		psql -h localhost -U libreborme < clean_dump.sql

run:
		docker-compose up -d
		./manage.py migrate --settings libreborme.settings_dev
		./manage.py runserver --settings libreborme.settings_dev
		# ./manage.py runserver_plus

shell:
		./manage.py shell_plus --settings libreborme.settings_dev

import:
		./manage.py importborme -f 2018-03-13 -t 2018-03-13 --local-only --settings libreborme.settings_dev

import1:
		./manage.py importbormejson /home/pablo2/.bormes/json/2018/03/13/BORME-A-2018-51-41.json --settings libreborme.settings_dev

import2:
		./manage.py importbormejson /home/pablo2/bormes_spider/json/2018/03/13/BORME-A-2018-51-41.json --settings libreborme.settings_dev

emailserver:
		./manage.py mail_debug

graph_model:
		# ./manage.py graph_models -a -g -o graph_model.png
		./manage.py graph_models borme libreborme alertas -g -o graph_model.png
		@echo "Generated graph_model.png"

test:
		DJANGO_SETTINGS_MODULE=libreborme.settings_ci DB_HOST=localhost ./manage.py test --noinput -v 3

test1:
		DJANGO_SETTINGS_MODULE=libreborme.settings_ci DB_HOST=localhost ./manage.py test --noinput -v 3 borme.tests.test_import.TestImport2.test_nombramientos_ceses

test2:
		./setup.py test

test3:
		./runtests.py

test_ci:
		./scripts/wait-for-it.sh elasticsearch:9200 --timeout=30
		coverage run --source='.' manage.py test --noinput -v 3
		coverage report

test_docker:
		echo `git rev-parse HEAD`
		docker build -t libreborme:ci .
		CONTAINER_IMAGE=libreborme CI_BUILD_REF_NAME=ci docker-compose -f docker-compose.ci.yml -p ci up --abort-on-container-exit

staging:
		./manage.py check
		./manage.py check --deploy
		./manage.py collectstatic --noinput
		./manage.py migrate
		./manage.py loaddata ./libreborme/fixtures/config.json
		./manage.py loaddata ./alertas/fixtures/alertasconfig.json
		uwsgi --ini=/site/uwsgi.ini

update_staging_images:
		# docker login -u gitlab-ci-token -p $CI_JOB_TOKEN registry.gitlab.com
		docker build -t registry.gitlab.com/libreborme/libreborme:staging .
		docker push registry.gitlab.com/libreborme/libreborme:staging
		cd docker/nginx && docker build -t registry.gitlab.com/libreborme/libreborme/nginx:staging .
		docker push registry.gitlab.com/libreborme/libreborme/nginx:staging
