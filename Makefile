RUN=poetry run

all: setup

setup:
	poetry install
	${RUN} pre-commit install
