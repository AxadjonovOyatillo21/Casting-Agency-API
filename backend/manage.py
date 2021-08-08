from src.api import app
from src.database.models import db, db_drop_and_create_all, append_data
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import os 

migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    app.run(debug=True)

@manager.command
def setup_db():
    db_drop_and_create_all()
    append_data()


@manager.command
def runtests():
    os.system("python3 test_app.py")


if __name__ == "__main__":
    manager.run()
