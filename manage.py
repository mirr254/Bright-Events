import os
from app import db, createApp
from app.events_blueprint import models

app = createApp(conf_name=os.getenv('APP_SETTINGS'))

from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()