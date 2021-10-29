# playstore-app-data
API to get information of app in playstore

# Installation

- Clone this repository and change directory.
- Installation using [Poetry](https://python-poetry.org/)(recommended).
```bash
poetry install
# OR without poetry
pip install -r requirements
```
- Run application
```bash
python wsgi.py
```

# Usage

Make a get request with app package id in query parameter.

Example: `https://localhost:5000?id=com.app.mirrorscore`
