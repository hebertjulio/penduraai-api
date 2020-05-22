release: python manage.py migrate
web: daphne penduraai.asgi:application --port 8888 --bind 0.0.0.0 -v2
