from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask.ext.script import Manager
from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, TextAreaField, FormField
from wtforms.validators import Required, DataRequired
from flask_sqlalchemy import SQLAlchemy
#from flask_login import login_required  #保护路由
import os
from flask_migrate import Migrate, MigrateCommand


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
manager = Manager(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
#  数据库迁移
migrate = Migrate(app, db)

# 初始化数据库连接:

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name


"""数据库初始化"""
class Safe(db.Model):
    __tablename__ = 'safe'
    id = db.Column(db.Integer, primary_key=True)
    order_num = db.Column(db.String(64), unique=True)
    main_num = db.Column(db.String(64), unique=True)
    sec_num = db.Column(db.String(64), unique=True)
    control_num = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Safe %r>' % self.order_num

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class NameForm(Form):
    name = StringField("你的名字？", validators=[Required()])
    role = StringField("角色", validators=[Required()])
    submit = SubmitField('登陆')

class Safe_form(Form):
    order_num = StringField("订单号：",validators=[Required()])
    main_num = StringField("主安全气囊：",validators=[Required()])
    sec_num = StringField("副安全气囊：",validators=[Required()])
    control_num = StringField("控制器：",validators=[Required()])
    submit = SubmitField('提交')


class PostForm(Form):
     title = StringField('标题', [DataRequired()])
     text = TextAreaField('内容', [DataRequired()])
     submit = SubmitField('登陆')


#@app.route('/secret')
#@login_required
#def secret():
#   return 'Only authenticated users are allowed!'


@app.route('/myfirst', methods=['GET', 'POST'])
def myfirst():
    form = Safe_form()
    if form.validate_on_submit():
        order_num = Safe.query.filter_by(order_num=form.order_num.data).first()
        if not order_num:
            num = Safe(order_num=form.order_num.data, main_num=form.main_num.data,
                       sec_num=form.sec_num.data, control_num=form.control_num.data)
            db.session.add(num)
            db.session.commit()
            session['order_num'] = form.order_num.data
            session['main_num'] = form.main_num.data
            session['sec_num'] = form.sec_num.data
            session['control_num'] = form.control_num.data
            form.order_num.data = ''
            form.main_num.data = ''
            form.sec_num.data = ''
            form.control_num.data = ''

        else:
            flash('输入订单重复，请重新输入')
            return redirect(url_for('myfirst'))

    return render_template('myfirst.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if not user:
            user1 = User(username=form.name.data)
            db.session.add(user1)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        session['role'] = form.role.data
        print(User.query.filter_by(username=form.name.data).all())
        print(session['role'])
        return redirect(url_for('user', name=session['name'],
                                role=session['role'], known=session['known'], _external=True))
    return render_template('index.html', form=form)


@app.route('/user-<name>-<role>-<known>')
def user(name, role, known):
    return render_template('user.html', name=name, role=role, known=known)


@app.route('/pyecharts')
def found():
    return render_template('pyecharts.html', myechart=scatter3d())


def scatter3d():
    from pyecharts import Scatter3D, Page,Bar

    import random
    page = Page()
    attr = ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"]
    v1 = [5, 20, 36, 10, 75, 90]
    v2 = [10, 25, 8, 60, 20, 80]
    bar = Bar("3D柱状图示例")
    bar.add('商家A', attr, v1)
    bar.add('商家B', attr, v2)
    page.add(bar)
    data = [[random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)] for _ in range(80)]
    range_color = ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf',
                   '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
    scatter3D = Scatter3D("3D 散点图 demo", width=1200, height=600)
    scatter3D.add("", data, is_visualmap=True, visual_range_color=range_color)
    page.add(scatter3D)
    return page.render_embed()

if __name__ == '__main__':
    manager.run()
