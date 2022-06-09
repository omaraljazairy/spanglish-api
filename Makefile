API_CONTAINER := api-spanglish-api
DB_CONTAINER := mysql-spanglish-api
POSTGRESQL_CONTAINER := postgresql-spanglish-api
help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
start:	## Start the docker container
	@docker-compose up -d
run:  ## run the server
	@uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
bash:	## enter the docker container bash
	@docker exec -it ${API_CONTAINER} bash
stop:	## stop the docker containers
	@docker-compose down
test:	## unittest the application using pytest
	@python -m pytest --cov=. tests/ --cov-report term --flake8 --isort
test-html:	## unittest the application using pytest and generate html report
	@python -m pytest --cov=. tests/ --cov-report html --flake8 --isort
mysql:	## access the test database
	@docker exec -it ${DB_CONTAINER} mysql -uroot -p
postgresql: ## access the test postgresql
	@docker exec -it ${POSTGRESQL_CONTAINER} psql Language root
git-tag:	## add the tags to the changelog.md file
	@git for-each-ref --sort=taggerdate --format='### %(color:green)%(refname:short)%(color:reset) %09 %(taggerdate) - %(taggername): %(subject)' refs/tags > CHANGELOG.md