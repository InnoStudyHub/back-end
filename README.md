# Study Hub API

![Build and deploy](https://github.com/InnoStudyHub/back-end/actions/workflows/studyhub_actions.yaml/badge.svg)

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

Build and run the project on your host:

```bash
pip install requirements.txt
```

## Docker and deployment

You also can get image from the DockerHub:

```bash
docker pull diazzzu/studyhub:studyhub_back
docker run diazzzu/studyhub:studyhub_back
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
