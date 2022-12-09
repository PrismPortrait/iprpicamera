#!/usr/bin/bash

sudo systemctl link /home/pi/iprpicamera/camera.service
sudo systemctl enable camera
sudo systemctl start camera
