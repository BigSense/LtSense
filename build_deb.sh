#!/bin/sh
fpm -t deb -s python --python-install-lib /usr/lib/python2.7/dist-packages --python-bin=$(which python2.7) --no-python-fix-name setup.py
