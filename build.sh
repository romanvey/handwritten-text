#!/usr/bin/env bash
set -e
set -x
docker build -t flask_gunicorn_app_image . -f src/deploy/app/Dockerfile
docker run -d --name flask_gunicorn_app -p 8000:8000 flask_gunicorn_app_image