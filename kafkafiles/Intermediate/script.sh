sudo systemctl start docker
cd kafka-broker
sudo docker compose up -d
cd ..
cd producer
sudo docker build -t producer .
sudo docekr run --net kaf-net producer
