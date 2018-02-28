#!/bin/bash
#docker-machine create ndimensionaltictactoe

#eval "$(docker-machine env ndimensionaltictactoe)"

docker-compose build
docker-compose up -d
docker-compose logs

export DOCK_IP=$(docker-machine ip ndimensionaltictactoe)
echo $DOCK_IP
