from exts import db
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
