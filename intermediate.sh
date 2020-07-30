ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}' > a
IP_ADD=$(cat a)
rm a
VAR="KAFKA_ADVERTISED_HOST_NAME=$IP_ADD"
sed -i "/KAFKA_ADVERTISED_HOST_NAME/c $VAR" ./.env
sudo systemctl start docker
sudo docker-compose down
echo "Starting up broker"
sudo docker-compose up -d
sleep 60 
#cd ./kafkafiles1/producer
#echo "Sending Dummy data"
#sudo docker build -t pro .
#sleep 20
#sudo docker run -d --net sccam_default pro
#cd ..
cd ./kafkafiles1/filter
echo "Buliding Intermediate Container"
sudo docker build -t filter .
sleep 30
echo "Intermediate Running , you can see DB object IDs"
sudo docker run --net sccam_default filter
