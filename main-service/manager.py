from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from main import app
from models import db

# Intantiate migration with app and db
migrate = Migrate(app, db)

# Create command to run migration
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Run manager
if __name__ == '__main__':
    manager.run()