#!/usr/bin/env bash
#Preparing the web servers for the deployment of web static and its root directory files..

#Update the Linux webmachine and then install the Nginx web server to all our webservers
sudo apt-get update
sudo apt-get install nginx -y

#Create the New folders
#-P option in mkdir means makedirectory then checkout
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
#fake html page
echo "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
   Moses Keep up!
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

#Symbolic link creation and if already exists, delete it and create a new one:

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

#Recursively change and give ownership to ubuntu user for data directory and its files.
sudo chown -R ubuntu:ubuntu /data/

#Configure Nginx to locate this location when url has a subentry.
sudo sed -i '39 i\ \tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n' /etc/nginx/sites-enabled/default
sudo service nginx restart
