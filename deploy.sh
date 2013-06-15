#! /bin/bash

apt-get install python-pip
pip install -r requirements.txt

python sensible_data_service/manage.py runserver 166.78.249.214:8082
