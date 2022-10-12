sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
pkill -f runserver

sudo docker login -u $LOGIN -p $PWD
sudo docker system prune --all -f
sudo docker-compose stop app
sudo docker-compose pull
sudo docker-compose up -d
