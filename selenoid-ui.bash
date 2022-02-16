#!/usr/bin/env bash
DOCKER_GATEWAY_ADDR=$(docker inspect selenoid -f '{{.NetworkSettings.Gateway}}')
echo "$DOCKER_GATEWAY_ADDR"
docker container rm selenoid-ui
docker run -d --name selenoid-ui -p 8080:8080 aerokube/selenoid-ui --selenoid-uri http://"${DOCKER_GATEWAY_ADDR}":4444
