from exts import db
from datetime import *


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    tel = db.Column(db.String(11),nullable=False)
    password1 = db.Column(db.String(20),nullable=False)


class Articles(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    title = db.Column(db.String(100), nullable=False,primary_key=True)
    content = db.Column(db.Text,nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    article = db.relationship('Users',backref=db.backref('article'))


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    articles_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    comment_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    article = db.relationship('Articles',backref=db.backref('comment'))

#    定义引用关系，不用重复查询数据库：
#    在Comments 表中定义 article = db.relationship('Articles',backref = db.backref('comment'))
#    可以通过my_articles.comment 访问 Comments 模型
#    也可以通过my_comments.artile 访问 Article 模型
#    default 设值该列的默认值，datatime.now()返回当前时间
