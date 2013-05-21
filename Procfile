web: gunicorn chatbot.wsgi -w 3
celeryd: python manage.py celeryd worker -E -B --loglevel=INFO
