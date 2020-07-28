
#!/bin/bash

curl -H "Metadata-Flavor: Google" http://169.254.169.254/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip > a
ip_add=$(cat a)
rm a
sudo sed -i '$ d' ~/.profile
sudo echo "IP_ADD=$ip_add" >> ~/.profile
.  ~/.profile

sudo systemctl start docker
sleep 20
cd kafka-broker
echo "removing older containers"
sudo docker-compose down
sleep 10
echo "Setting up Broker"
sleep 10
sudo docker-compose up -d
sleep 50
cd ..
cd producer
echo "Setting up producer"
sudo docker build -t producer .
sleep 20
echo "Running producer"
sudo docker run --net kaf-net producer
