#!/usr/bin/env bash
set -e
set -x
docker stop ngnix_server
docker rm ngnix_server
docker rmi ngnix_server_image
docker volume prune -f