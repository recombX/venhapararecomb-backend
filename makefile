export FLASK_ENV := development

all:
	echo FLASK_ENV: $$FLASK_ENV
	flask run

clean_db_uploads:
	rm -rf database.db uploads/*

init_env:
	python3 -m venv env
	. env/bin/activate
	pip install -r requirements.txt






