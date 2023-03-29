#!/bin/bash

if [[ "$(docker ps -aq -f name="$PROJECT_NAME" 2>/dev/null)" != "" ]]; then
  echo "stopped container $PROJECT_NAME"
  docker rm "$(docker stop "$(docker ps -aq -f name="$PROJECT_NAME")")"
fi

docker run --network host -d --restart always --name "$PROJECT_NAME" -it "$PROJECT_NAME":"$LAST_TAG"
