1. Change bootstrap_servers to the external IP address of the intermediate VM .
2. Build a docker image
  > sudo docker build -t consumer .
3. Run docker container 
  > sudo docker run -p 8050:8050 -p 9092:9092 consumer 
4. Open the hosted webpage with (external IP of backend):8050
