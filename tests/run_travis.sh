#!/usr/bin/env bash
python test_app_tests.py > /dev/null &
nosetests --with-coverage