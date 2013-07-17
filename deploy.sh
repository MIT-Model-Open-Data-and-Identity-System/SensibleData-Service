#! /bin/bash

apt-get install python-pip
pip install -r requirements.txt

python sensible_data_service/manage.py runserver $1:$2
