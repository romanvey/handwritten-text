#!/usr/bin/env bash
set -e
set -x
docker build -t ngnix_server_image src -f src/deploy/ngnix_server/Dockerfile
docker run -d --name ngnix_server -p 8080:80 ngnix_server_image