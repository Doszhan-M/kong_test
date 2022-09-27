#!/bin/bash

echo "BUILD KONG"
docker build -t registry.gitlab.com/uchet.kz/pk/deploy/dev/kong:latest -f ./kong/kong.dockerfile ./kong
echo "----------------------------------------------"


echo "PUSH KONG"
docker push registry.gitlab.com/uchet.kz/pk/deploy/dev/kong:latest
echo "----------------------------------------------"

