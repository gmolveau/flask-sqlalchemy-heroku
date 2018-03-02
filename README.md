# Boilerplate for a flaskk based app with sqlalchemy and postgresql, deploy easily on heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

dependencies used in the virtual_env :

`flask flask-sqlalchemy flask-script gunicorn psycopg2 flask-marshmallow requests python-dotenv flask-bcrypt marshmallow-sqlalchemy`

Install the app and environment :

```bash
git clone https://github.com/gmolveau/flask-sqlalchemy-heroku
cd flask-sqlalchemy-heroku
virtualenv venv -p python3
source venv/bin/activate
pip3 install -r requirements.txt
```

Test the app :

```bash
# if the heroku toolbelt is installed
heroku local

# else if on unix
gunicorn wsgi:app

# else if on windows
python3 wsgi.py
```

Test the stack (with docker) :
```bash
docker-compose up --build

# or in the background with
docker-compose up --build -d
```

Schedule a task for free every 10 minutes, every hour, or every day with heroku-scheduler :

For example, execute this script :

`python3 manage.py scheduleTime`
