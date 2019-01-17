# Questioner API
[![Build Status](https://travis-ci.org/j0nimost/Questioner.svg?branch=develop)](https://travis-ci.org/j0nimost/Questioner) [![codecov](https://codecov.io/gh/j0nimost/Questioner/branch/develop/graph/badge.svg)](https://codecov.io/gh/j0nimost/Questioner) [![Maintainability](https://api.codeclimate.com/v1/badges/9afd47aa96de42fcf690/maintainability)](https://codeclimate.com/github/j0nimost/Questioner/maintainability)


This is Andela's Bootcamp Challenge two. The challenge is to create an API implementation for Questioner.

## Summary
The Questioner API will not use a database instead it uses data structures to store data in memory. The Questioner API uses the Flask framework for development. The Questioner API will handle features from questions and meetups.

### Version
The API versioning corresponds to the challenges being done; The prefix for versioning the API is `api/v<number>`

## V1
This is the first version `v1` of the api. This Version consists of Challenge 2, endpoints. To access this version in the folder structure use `app/api/v1`. Tests for this version are located in `app/tests/v1` folder.

## V2
This is the second version `v2` of the api. This version consists of Challenge 3 endpoints. To access this version in the folder structure use `app/api/v2`. Tests for this version are located in `app/tests/v2` folder.

## Features

| Task | Request |  Endpoint|
| --- | --- | --- |
| Create Meetup | POST | `/meetups` |
| Get Meetup | GET | `/meetups/<id>` |
| Get Meetups | GET | `/meetups/upcoming` |
| Create Question | POST | `/questions` |
| Upvote Question | PATCH | `/questions/<id>/upvote` |
| Downvote Question | PATCH | `/questions/<id>/downvote` |
| RSVP Meetup | POST | `/meetups/<id>/rsvps` |

## Pivotal Tracker
[This](https://www.pivotaltracker.com/n/projects/2235178) is the link to the Pivotal Stories. The Stories for develop are under the label `api`

## Requirements
These are the basic requirements required to run Questioner API;

- Python 3.0 >
- Virtualenv 
- ...Others in `requirements.txt`

## Testing

Run the following commands subsequently.
- `git clone https://github.com/j0nimost/Questioner.git`
- `cd Questioner/`
- `virtualenv env`
- `source .env`
- `pip install -r requirements.txt`
- `flask run`

## Author
John Nyingi
