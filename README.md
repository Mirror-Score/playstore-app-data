# PlayStore App Data
API to get information of app in playstore

This API is currently intended to use for checking the current version of app in Google playstore to compare with installed version of app in device.

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

# Upcoming features
Add other searchable parameters like name, title, keyworks, etc.

# TODO
- [ ] Add unit test.
- [ ] Add other searchable parameters.
- [ ] Add better error handling and loggin to API.
- [ ] Make dir structure organised and handle environment.
- [ ] Setup Docker and Heroku deployment.
- [ ] Setup contributions and issue guidelines.

# Contribution
PRs are welcome :handshake: for new feature and bug fixes. If you would like to help. [TODO](#todo) is good place to start.

# License
This project is licensed under [MIT License](LICENSE)
