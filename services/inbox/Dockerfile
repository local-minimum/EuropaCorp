FROM python:3

COPY "requirements.txt" "/tmp/requirements.txt"
RUN ["pip", "install", "-r", "/tmp/requirements.txt"]

RUN mkdir /var/run/prometheus_multiproc
ENV prometheus_multiproc_dir=/var/run/prometheus_multiproc

COPY src/ /app/
WORKDIR /app
ENTRYPOINT ["python", "-m", "inbox"]
