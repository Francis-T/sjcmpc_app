#!/bin/sh

echo $PWD
cd /home/pi/Programs/sjcmpc_app/

sudo pip3 install Rpi.GPIO

cd SPI-Py
python3 setup.py build
python3 setup.py install

cd ..
sudo apt install libmysqlclient-dev
sudo apt install default-libmysqlclient-dev

sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
sudo apt pkg-config libgl1-mesa-dev libgles2-mesa-dev
sudo apt python-setuptools libgstreamer1.0-dev git-core python-dev libmtdev-dev xclip
sudo apt install gstreamer1.0-plugins-bad
sudo apt install gstreamer1.0-plugins-base
sudo apt install gstreamer1.0-plugins-good
sudo apt install gstreamer1.0-plugins-ugly
sudo apt install gstreamer1.0-omx
sudo apt install gstreamer1.0-alsa

sudo pip3 install -U Cython==0.25.2
sudo pip3 install pygments
sudo pip3 install docutils
sudo pip3 install sqlalchemy
sudo pip3 install mysqlclient

if [ ! -d kivy ];
then
    git clone https://github.com/kivy/kivy
    cd kivy
    make
    echo "export PYTHONPATH=$(pwd):\$PYTHONPATH" >> ~/.profile
    source ~/.profile
fi;


