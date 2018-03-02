FROM alpine:3.7

RUN apk update && \
    apk add --no-cache bash postgresql-client python3 py3-psycopg2 && \
    mkdir /flask_app

ADD . /flask_app
WORKDIR /flask_app
RUN pip3 install -r docker.requirements.txt && chmod +x wait-for-postgres.sh manage.py

EXPOSE 5000

CMD /flask_app/wait-for-postgres.sh db && python3 manage.py resetdb && /usr/bin/gunicorn -b :5000 wsgi:app
