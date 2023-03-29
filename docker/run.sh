#!/bin/bash

if [[ "$(docker ps -aq -f name="$PROJECT_NAME" 2>/dev/null)" != "" ]]; then
  docker rm "$(docker stop "$(docker ps -aq -f name="$PROJECT_NAME")")"
fi

docker run --network host -d --restart always \
  -e TG_TOKEN="$TG_TOKEN" \
  -e PG_USER="$PG_USER" \
  -e PG_SCHEMA="$PG_SCHEMA" \
  -e PG_PASSWORD="$PG_PASSWORD" \
  --name "$PROJECT_NAME-$POSTFIX" \
  -it "$PROJECT_NAME":"$TAG_PROJECT"
