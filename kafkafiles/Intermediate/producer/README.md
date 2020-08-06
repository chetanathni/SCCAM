1. Build a docker image
> sudo docker build -t producer .
2. Run the docker image
> sudo docker run --net kaf-net producer -v /var/run/docker.sock:/var/run/docker.sock

