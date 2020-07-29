sudo systemctl start docker
cd ./kafkafiles/Edge
echo "Building the image"
sudo docker build -t edge .
sleep 30
echo "Running Edge"
sudo docker run edge
