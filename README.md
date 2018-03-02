# Flask boilerplate facebook messenger bot


dependencies : `flask flask-sqlalchemy flask-script gunicorn psycopg2 flask-marshmallow requests python-dotenv flask-bcrypt marshmallow-sqlalchemy`


```bash
git clone https://github.com/gmolveau/flask-messenger-bot
cd flask-messenger-bot
virtualenv venv -p python3
source venv/bin/activate
pip3 install -r requirements.txt

# on unix
gunicorn wsgi:app

# on windows
python3 wsgi.py
```

`docker-compose up --build -d`


`example of a schedule action`

with the heroku scheduler, call every 10 minutes the script :

`python3 manage.py scheduleTime`
