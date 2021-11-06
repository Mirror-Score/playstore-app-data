API to get information of app in playstore

This API is currently intended to use for checking the current version of app 
in Google playstore to compare with installed version of app in device.

# Table of Contents
- [Table of Contents](#table-of-contents)
- [Installation](#installation)
  - [pre-requisite](#pre-requisite)
  - [Setup instructions](#setup-instructions)
- [Usage](#usage)
- [Upcoming features](#upcoming-features)
- [TODO](#todo)
- [Contribution](#contribution)
- [License](#license)

# Installation

## pre-requisite
- [Poetry](https://python-poetry.org/)
- Python-3.8 or above
- Git

## Setup instructions
- Clone this repository and change directory.
```bash
git clone https://github.com/Mirror-Score/playstore-app-data
cd playstore-app-data
```
- Install setup
```bash
make
```

# Usage

Make a get request with app package id in query parameter.

Example: `https://localhost:5000?id=com.app.mirrorscore`

# Upcoming features
Add other searchable parameters like name, title, keyworks, etc.

# TODO
- [ ] Add unit test.
- [ ] Add other searchable parameters.
- [ ] Add better error handling and logging to API.
- [ ] Make dir structure organised and handle environment.
- [ ] Setup Docker and Heroku deployment.
- [ ] Setup contributions and issue guidelines.

# Contribution
PRs are welcome :handshake: for new feature and bug fixes. If you would like to help. [TODO](#todo) is good place to start.

# License
This project is licensed under [MIT License](LICENSE)
