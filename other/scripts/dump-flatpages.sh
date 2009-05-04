#!/bin/bash
#
cd /home/www-data/determine/django/determine/
python manage.py dumpdata flatpages --indent=2 --format=xml >./flatpages.xml
