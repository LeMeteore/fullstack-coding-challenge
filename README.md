# Unbabel Fullstack Challenge

Hey :smile:

Welcome to our Fullstack Challenge repository. This README will guide you on how to participate in this challenge.

In case you are doing this to apply for our open positions for a Fullstack Developer make sure you first check the available jobs at [https://unbabel.com/jobs](https://unbabel.com/jobs)

Please fork this repo before you start working on the challenge. We will evaluate the code on the fork.

**FYI:** Please understand that this challenge is not decisive if you are applying to work at [Unbabel](https://unbabel.com/jobs). There are no right and wrong answers. This is just an opportunity for us both to work together and get to know each other in a more technical way.

## Challenge


#### Build a multilingual Hackernews.

Create a multilingual clone of the Hackernews website, showing just the top 10 most voted news and their comments.
This website must be kept updated with the original hackernews website (every 10 minutes).

Translations must be done using the Unbabel API in sandbox mode.

Build a dashboard to check the status of all translations.


#### Requirements
* Use Flask web framework
* Use Bootstrap
* For MongoDB
* Create a scalable application.
* Only use Unbabel's Translation API on sandbox mode
* Have the news titles translated to 2 languages
* Have unit tests


#### Notes
* We dont really care much about css but please dont make our eyes suffer.
* Page load time shouldnt exceed 2 secs


#### Resources
* Unbabel's API: http://developers.unbabel.com/
* Hackernews API: https://github.com/HackerNews/API

#### What I've done:
* Clone the DiMesq's repository, containing already a good amount of what should be done.
* Ask of credential to use the unbabel API
* Create a virtualenv: python3 -m venv ~/envs/fsc
* Install everything necessary, and create a requirements.txt: pip freeze > requirements.txt
* Install mongodb: apt install mongodb
* Create the database folder, and make it writable by me: sudo mkdir /data/db && sudo chown $(id -u) /data/db
* Fix indentation, use print() instead of print
* use items() instead of iteritems() for dict objects
* instead of a Story object pass a json string to delay() using .to_json() method
* use f-strings instead of .format()
* wrap requests call inside try/except blocks
* add settings for tests
* add a little bit of unit testing

#### To run the project:
* start mongodb: sudo mongod
* start celery worker that will receive tasks: celery --loglevel=DEBUG -A app.celery worker
* start the celery beat that will send tasks to worker: celery beat -A app.celery --loglevel=DEBUG
* start application: ./run.py

#### To run the tests:
* set env variable pointing to testing configuration then call test.py: TEST_SETTINGS="/home/nsukami/GITHUB/fullstack-coding-challenge/test_settings.py" python tests.py

### Todos:
* add Nginx + Gunicorn configuration files
* add deployment script, using fabric or ansible
* put secrets out of source code, for example, inside var envs
* fix all the mongoengine DeprecationWarnings
* improve tests
