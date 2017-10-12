#!/bin/sh

sudo pip3 install Rpi.GPIO

cd SPI-py
python3 setup.py build
python3 setup.py install

cd ..
sudo apt install libmysqlclient-dev
sudo pip3 install -U Cython==0.25.2
sudo pip3 install pygments
sudo pip3 install docutils
sudo pip3 install sqlalchemy
sudo pip3 install mysqlclient

if [ -d kivy ];
then
    git clone https://github.com/kivy/kivy
    cd kivy
    make
    echo "export PYTHONPATH=$(pwd):\$PYTHONPATH" >> ~/.profile
    source ~/.profile
fi;


