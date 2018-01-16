#!flask/bin/python
import os

from app import createApp

config_name = "development"

app = createApp(config_name)

if __name__ == '__main__':
    app.run(host='0.0.0.0')