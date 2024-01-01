# Description

simply wrapper around the strava API
+ [Get Your Strava Activity Data using Python (2023)](https://medium.com/@lejczak.learn/get-your-strava-activity-data-using-python-2023-️-b03b176965d0)+ https://developers.strava.com/docs/reference/
+ https://developers.strava.com/docs/authentication/

# Docker

1. Build docker image locally
```sh
docker build --tag ludw-strava .
```

2. Run as standalone docker container
```sh
docker run -d -p 5000:5000 --env CLIENT_ID --env CLIENT_SECRET --env REFRESH_TOKEN ludw-strava
```

3. Run as docker compose (remember to create `.env` file with all environmental variables)
```
version: '3'
services:

  strava-service:
    image: ludw-strava
    container_name: strava
    environment:
      - CLIENT_ID=${CLIENT_ID}
      - CLIENT_SECRET=${CLIENT_SECRET}
      - REFRESH_TOKEN=${REFRESH_TOKEN}
```