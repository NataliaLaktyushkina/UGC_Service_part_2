#!/bin/sh

echo "Waiting for Mongo DB..."

while ! nc -z mongodb 27017; do
  sleep 2
done

echo "Mongo DB started"

gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8101 main:app
