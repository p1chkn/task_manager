FROM python:3.6.9

WORKDIR /code
COPY . .
RUN pip install -r requirements.txt
CMD gunicorn task_manager.wsgi:application --bind 0.0.0.0:8000