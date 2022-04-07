FROM python:3.7-slim-bullseye

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
RUN pip install .

ARG app_host="0.0.0.0"
ARG app_port=8000

ENV FLASK_HOST=$app_host
ENV FLASK_PORT=$app_port

CMD [ "gunicorn", "wsgi:app", "wsgi.py" ]