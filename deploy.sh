export $(grep -v '^#' ~/.env | xargs)
pkill -f runserver

sudo docker login -u $DOCKER_LOGIN -p $DOCKER_PASSWORD
sudo docker system prune --all -f
sudo docker compose down
sudo docker compose pull
sudo docker compose up -d
