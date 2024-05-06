dev:
	poetry run flask --app page_analyzer:app run --debug

PORT ?= 8000
start:
	poetry run gunicorn -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	poetry run flake8 page_analyzer

build:
	./build.sh