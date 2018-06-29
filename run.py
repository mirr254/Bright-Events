#!flask/bin/python
import os

from app import createApp
from flask_mail import Mail

config_name = os.getenv('APP_SETTINGS') #"development"

app = createApp(config_name)
mail = Mail(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')