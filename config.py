import os
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
#SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'data_dev.sqlite')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/flaskdm?utf8'
SECRET_KEY = 'hard'
SQLALCHEMY_COMMIT_ON_TEARDOWN = False





