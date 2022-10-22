web: gunicorn --bind 0.0.0.0:8000 lifeingermany.wsgi --log-file -
celery: celery -A lifeingermany worker -l INFO
