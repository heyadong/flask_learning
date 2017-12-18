# import os
# from app import create_app, db
# from app.models import User, Role
# from flask_script import Manager, Shell
# from flask_migrate import Migrate, MigrateCommand
# #  获得app
# #  和数据库相关的文件放到一起
# app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# manager = Manager(app)
# migrate = Migrate(app, db)
#
#
# def make_shell_context():
#     return dict(app=app, db=db, User=User, Role=Role)
#
# manager.add_command("shell", Shell(make_context=make_shell_context))
# manager.add_command('db', MigrateCommand)
# if __name__ == '__main__':
#     manager.run()

from flask_script import Manager
from flask_hyd import app
from flask_migrate import Migrate, MigrateCommand
from exts import db
from models import Users,Articles

manger = Manager(app)
migrate = Migrate(app, db)
manger.add_command('db', MigrateCommand)
if __name__ == '__main__':
    manger.run()