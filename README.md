# Handwritten text generator
You can start your server everywhere with simple commands

## Requirements
* Docker (install using `bash install_docker.sh`)

#### Install and run:
```
docker build -t flask_gunicorn_app_image . -f src/deploy/app/Dockerfile
docker run -d --name flask_gunicorn_app -p 8000:8000 flask_gunicorn_app_image
```
Or alternatively:
```
bash build.sh
```

#### Start:
```
docker start flask_gunicorn_app
```

#### Stop:
```
docker stop flask_gunicorn_app
```

#### Logs:
```
docker logs flask_gunicorn_app
```

#### Remove:
```
docker stop flask_gunicorn_app
docker rm flask_gunicorn_app
docker rmi flask_gunicorn_app_image
docker volume prune -f
```
Or alternatively:
```
bash remove.sh
```

#### Local build:
```
bash local_build.sh
```

##### Developed by: Roman Vey, Volodymyr Zabulskyy and Vasyl Borsuk