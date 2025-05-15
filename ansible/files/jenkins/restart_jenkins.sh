#!/bin/bash

cd /var/tmp/docker/jenkins || exit 4
docker compose down && docker compose up -d || exit 5
