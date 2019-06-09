set -e
set -x
curl https://get.docker.com/ | bash
sudo usermod -aG docker $USER
docker --version

sudo curl -L "https://github.com/docker/compose/releases/download/1.23.1/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
