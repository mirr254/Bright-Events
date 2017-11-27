#!/usr/bin/env bash
python app.py > /dev/null &
nosetests tests/ --with-coverage