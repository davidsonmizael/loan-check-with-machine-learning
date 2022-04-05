FROM python:3.7-slim-bullseye

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

RUN pip install .

CMD [ "gunicorn", "wsgi:app", "app.py" ]