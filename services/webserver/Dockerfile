FROM python:3

RUN ["pip", "install", "gunicorn"]
COPY "requirements.txt" "/tmp/requirements.txt"
RUN ["pip", "install", "-r", "/tmp/requirements.txt"]

RUN mkdir /var/run/prometheus_multiproc
ENV prometheus_multiproc_dir=/var/run/prometheus_multiproc

COPY src/ /app/
WORKDIR /app
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:5000"
EXPOSE 5000
ENTRYPOINT ["gunicorn", "webserver:app"]
