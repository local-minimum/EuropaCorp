FROM python:3.6

COPY "requirements.txt" "/tmp/requirements.txt"
RUN ["pip", "install", "-r", "/tmp/requirements.txt"]

COPY src/ /app/
WORKDIR /app
ENTRYPOINT ["python", "-m", "inbox"]
