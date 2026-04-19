setup:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt
	python -m pip install -r requirements-dev.txt
	python manage.py migrate
	python manage.py check

run:
	python manage.py runserver

test:
	python manage.py test

quality:
	black --check .
	isort --check-only .
	flake8 .
	pytest
