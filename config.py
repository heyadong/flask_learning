import os
import pymysql
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
pymysql.install_as_MySQLdb()
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data_dev.sqlite')
# SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/flaskdm?utf8'
SECRET_KEY = 'hard'
SQLALCHEMY_COMMIT_ON_TEARDOWN = False





