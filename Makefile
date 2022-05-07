help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
start:	## Start the docker container
	@docker-compose up -d
run:  ## run the server
	@uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
bash:	## enter the docker container bash
	@docker exec -it api-spanglish-api bash
stop:	## stop the docker containers
	@docker-compose down
test:	## unittest the application using pytest
	@python -m pytest --cov=. tests/ --cov-report term --flake8 --isort
test-html:	## unittest the application using pytest and generate html report
	@python -m pytest --cov=. tests/ --cov-report html --flake8 --isort
