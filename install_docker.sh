set -e
set -x
curl https://get.docker.com/ | bash
sudo usermod -aG docker $USER
docker --version
