from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app, db
from app.models import Admin

app = create_app()
manager = Manager(app)

# Add Flask-Migrate commands to Flask-Script manager
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def create_tables():
    """Creates all database tables."""
    db.create_all()

@manager.command
def drop_tables():
    """Drops all database tables."""
    db.drop_all()

@manager.command
def recreate_tables():
    """Recreates all database tables."""
    drop_tables()
    create_tables()

if __name__ == '__main__':
    manager.run() 