#!/bin/bash

if [[ "$(docker ps -aq -f name="$PROJECT_NAME" 2>/dev/null)" != "" ]]; then
  docker rm "$(docker stop "$(docker ps -aq -f name="$PROJECT_NAME")")"
fi

docker run --network host -d --restart always \
  -e TG_TOKEN="$TG_TOKEN" \
  -e PG_USER="$PG_USER" \
  -e PG_SCHEMA="$PG_SCHEMA" \
  -e PG_PASSWORD="$PG_PASSWORD" \
  -e PG_DB="$PG_DB" \
  -e PG_PORT="$PG_PORT" \
  -e PG_HOST="$PG_HOST" \
  --name "$PROJECT_NAME" \
  -it "$PROJECT_NAME":"$1"
