#!/usr/bin/env bash
set -e
set -x
docker stop flask_gunicorn_app
docker rm flask_gunicorn_app
docker rmi flask_gunicorn_app_image
docker volume prune -f