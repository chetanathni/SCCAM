sudo systemctl start docker
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi $(sudo docker images)
cd kafka-broker
sudo docker compose up -d
cd ..
cd producer
sudo docker build -t producer .
sudo docker run --net kaf-net producer -d
