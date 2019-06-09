First start:
docker build -t flask_gunicorn_app .
docker run -d --name flask_gunicorn_app -p 8000:8000 flask_gunicorn_app

Start:
docker start flask_gunicorn_app

Stop:
docker stop flask_gunicorn_app

Logs:
docker logs flask_gunicorn_app

Remove:
docker stop flask_gunicorn_app
docker rm flask_gunicorn_app
docker rmi flask_gunicorn_app
docker volume prune -f
