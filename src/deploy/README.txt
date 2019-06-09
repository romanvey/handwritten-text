# Flask app

First start:
docker build -t flask_gunicorn_app_image .
docker run -d --name flask_gunicorn_app -p 8000:8000 flask_gunicorn_app_image

Start:
docker start flask_gunicorn_app

Stop:
docker stop flask_gunicorn_app

Logs:
docker logs flask_gunicorn_app

Remove:
docker stop flask_gunicorn_app
docker rm flask_gunicorn_app
docker rmi flask_gunicorn_app_image
docker volume prune -f

# NGNIX app
TODO: write desc
