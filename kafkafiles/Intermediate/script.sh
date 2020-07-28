curl -H "Metadata-Flavor: Google" http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip > a
ip_add=$(cat a)
rm a
sudo sed -i '$ d' ~/.profile
sudo echo "IP_ADD=$ip_add" >> ~/.profile
.  ~/.profile
sudo echo "KAFKA_ADVERTISED_HOST_NAME: $ip_add" >> .env
sudo systemctl start docker
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi $(sudo docker images)
cd kafka-broker
sudo docker-compose up -d
sleep 10
cd ..
cd producer
sudo docker build -d -t producer .
sudo docker run --net kaf-net producer