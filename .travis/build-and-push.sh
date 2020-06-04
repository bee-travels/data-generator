#!/bin/bash
echo "TRAVIS COMMIT $TRAVIS_COMMIT"
docker build -t beetravels/data-gen-destination:$TRAVIS_COMMIT src/destination
docker build -t beetravels/data-gen-carrental:$TRAVIS_COMMIT src/car_rental
docker build -t beetravels/data-gen-hotel:$TRAVIS_COMMIT src/hotels
docker build -t beetravels/data-gen-airports:$TRAVIS_COMMIT src/airports

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

docker push beetravels/data-gen-destination:$TRAVIS_COMMIT
docker push beetravels/data-gen-carrental:$TRAVIS_COMMIT
docker push beetravels/data-gen-hotel:$TRAVIS_COMMIT
docker push beetravels/data-gen-airports:$TRAVIS_COMMIT
