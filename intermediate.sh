sudo systemctl start docker
sudo docker-compose down
echo "Starting up broker"
sudo docker-compose up -d
sleep 60 
cd ./kafkafiles1/producer
echo "Sending Dummy data"
sudo docker build -t pro .
sleep 20
sudo docker run -d --net package_default pro
cd ..
cd ./filter
echo "Buliding Intermediate Container"
sudo docker build -t filter .
sleep 30
echo "Intermediate Running , you can see DB object IDs"
sudo docker run --net package_default filter
