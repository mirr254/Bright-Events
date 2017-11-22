#!/usr/bin/env bash
python tests/test_app_tests.py > /dev/null &
nosetests --with-coverage