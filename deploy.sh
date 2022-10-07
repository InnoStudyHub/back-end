sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
pkill -f runserver

sudo set -o allexport
sudo source .ssh/environment
sudo docker login -u $DOCKER_LOGIN -p $DOCKER_PWD
sudo docker system prune --all -f
sudo docker-compose down
sudo docker-compose pull
sudo docker-compose up -d
