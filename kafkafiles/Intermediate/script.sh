
#!/bin/bash

sudo systemctl start docker
sleep 20
cd kafka-broker
echo "removing older containers"
sudo docker-compose down
sleep 10
echo "Setting up Broker"
sleep 10
sudo docker-compose up
