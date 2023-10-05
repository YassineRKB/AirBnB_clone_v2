#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# Exit on errors
set -e

## apt operations
sudo apt update -y
sudo apt install nginx -y

## vars & configs setup
ALX_base="/data/web_static"
ALX_tests="$ALX_base/releases/test"
ALX_shared="$ALX_base/shared"
ALX_index="$ALX_tests/index.html"
ALX_current="$ALX_base/current"
ALX_nginxSites="/etc/nginx/sites-available/default"

## dirs, pers & ownershipt operatopns
sudo mkdir -p "$ALX_tests" "$ALX_shared"
echo 'Hello World!' | sudo tee "$ALX_index" > /dev/null
sudo ln -sfn "$ALX_tests" "$ALX_current" 
chown -R ubuntu:ubuntu "$ALX_base"

## nginx configs
nginx_config="location /hbnb_static/ { alias $ALX_current/; }"
sudo sed -i "/listen 80 default_server/a $nginx_config" "$ALX_nginxSites"

## nginx service
sudo service nginx restart
