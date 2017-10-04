#!/bin/sh

pip3 install Rpi.GPIOe

cd SPI-py
python setup.py build
python setup.py install

sudo apt install libmysqlclient-dev
pip3 install sqlalchemy
pip3 install mysqlclient



