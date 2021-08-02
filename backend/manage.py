from src.api import app
from src.database.models import db
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
def runtests():
    os.system("python tests/test_api.py")

@manager.command
def salom():
    return {
        "message": "Assalomu alaykum!"
    }


@manager.command
def sifatsiz_ekansan():
    return {
        "message": "Tur yo'qol!"
    }


if __name__ == "__main__":
    manager.run()
