sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
pkill -f runserver

set -o allexport
source .ssh/environment
(envsubst < deploy.sh) > docker-compose.yaml

sudo docker login -u $DOCKER_LOGIN -p $DOCKER_PWD
sudo docker system prune --all -f
sudo docker-compose down
sudo docker-compose pull
sudo docker-compose up -d
