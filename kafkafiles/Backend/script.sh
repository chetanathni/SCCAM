sudo systemtl start docker
sudo docker rm $(sudo docker ps -aq)
sudo dokcker rmi $(sudo docker images)
cd consumer
sudo docker build -t consumer .
sudo docker run -p 8050:8050 -p 9092:9092 consumer 