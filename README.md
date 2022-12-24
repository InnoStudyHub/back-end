# Study Hub API
[![Deploy](https://github.com/InnoStudyHub/back-end/actions/workflows/build_and_deploy.yaml/badge.svg)](https://github.com/InnoStudyHub/back-end/actions/workflows/build_and_deploy.yaml)
[![Django Test](https://github.com/InnoStudyHub/back-end/actions/workflows/django_test.yaml/badge.svg)](https://github.com/InnoStudyHub/back-end/actions/workflows/django_test.yaml)
[![Linter](https://github.com/InnoStudyHub/back-end/actions/workflows/django_linter.yaml/badge.svg)](https://github.com/InnoStudyHub/back-end/actions/workflows/django_linter.yaml)

## About the project

### Problem

As Innopolis University students we noticed the lack of time problem while preparing to the exams. Students try to find the materials used by previous years for exam preparation in telegram chats to use their time more efficient.

### Solution

So, we introduce an application that will store the materials for exam preparation.

It is a crowdsourcing educational application aimed towards Innopolis University students. The app is directed to ease the process of the material assimilation and exam preparation.

The idea is to store the courses material in the form of cards, where one side is a question, another - answer.

## Prerequisites

For this project you need to have Python installed on your machine. You can see instructions [here](https://www.python.org/downloads/).

## How to use

Clone the repo into your folder:

```bash
git clone https://github.com/InnoStudyHub/back-end.git
cd ./back-end
```

Install requirements:
```bash
pip install requirements.txt
```

Run application
```bash
python manage.py runserver localhost:{port}
```

Application will open in
```bash
http://localhost:{port}
```

Health check
```bash
http://localhost:{port}/api/health_check/
```

Swagger
```bash
http://localhost:{port}/api/schema/swagger-ui/#/
```

## Docker and deployment

You also can run application via docker:

```bash
docker-compose up
```

Deployed version of application is available:
```bash
http://api-dev.studyhub.kz:8000
http://api-dev.studyhub.kz:8000/api/health_check/
http://api-dev.studyhub.kz:8000/api/schema/swagger-ui/#/
```

## Tests

The tests can be run in the project with the command

```bash
python manage.py test
```

## How to contribute

Fork this repository, make changes, send us a pull request. We will review your changes and apply them to the master branch if they don't violate the quality standards.

We are planning to add:

- raiting system in a form of likes and dislikes
- privacy via deck access levels and study groups
- discussions in comments under the cards
- raiting of users to increase the crowdsourcing motivation
