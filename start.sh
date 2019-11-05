#!/bin/bash -a
source /var/local/.euco.env

cd services/ui && npm install && npm run build
docker-compose up --build -d
