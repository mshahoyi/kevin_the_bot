.PHONY: install format lint test clean run

run:
	python src/main.py

run-dev:
	nodemon -e py --exec make run

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

format:
	black src/

lint:
	flake8 src/

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete 