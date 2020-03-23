
from flask_migrate import MigrateCommand
from evento import manager

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
