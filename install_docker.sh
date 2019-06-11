curl https://get.docker.com/ | bash
sudo usermod -aG docker $USER
newgrp docker
sudo systemctl start docker
docker --version