#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, render_template,request,g ,session
import config
from exts import db
from models import Users,Articles
import os
app = Flask(__name__)
# 导入配置文件config.py
app.config.from_object(config)
#  注册db到app
db.init_app(app)
# 需要上下文处理器才能创建数据库
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    context = {
        'questions': Articles.query.filter_by(author_id=session.get('user_id')).all(),
        'author': Users.query.filter_by(id=session.get('user_id')).first()
    }
    print(context)
    print(session.get('user_id'))
    return render_template('indext.html', **context)



# @app.before_request
# def my_befor_request():
#     print('hello,nihao')

# 登陆页面视图函数
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login2.html')
    else:
        tellphone = request.form.get('tel')
        password = request.form.get('password1')
        user = Users.query.filter_by(tel=tellphone,password1=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return "登陆用户或者密码输入错误，请重新输入"

# 钩子函数（hook) context_processor 装饰器，返回字典，所有页面都可用
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = Users.query.filter_by(id=user_id).first()
        return {'user': user}
    else:
        return {}


# 注册视图函数
@app.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'GET':
       return render_template('register.html')
    else:
        name = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        tel = request.form.get('tel')
        if password1 != password2:
            return "密码不正确"
        else:
            user = Users(username=name,tel=tel,password1=password1)
            db.session.add(user)
            db.session.commit()
            return '注册成功'

# 文章发布视图函数

@app.route('/article/',methods=['GET','POST'])
def article():
    if request.method == 'GET':
        return render_template('article.html')
    else:
        a_id = session.get('user_id')
        a_title = request.form.get('theme')
        a_content = request.form.get('content')
        articles = Articles(author_id=a_id,title=a_title,content=a_content)
        db.session.add(articles)
        db.session.commit()
        return '发布成功'

# 注销
@app.route('/login_out/')
def login_out():
    # session.pop('user_id')
    del session['user_id']
    return redirect(url_for('register'))

# 笔记详情页面
@app.route('/detail/<question_id>')
def detail(question_id):
    content = Articles.query.filter_by(id=question_id).first()
    author = Users.query.filter_by(id=content.author_id).first()
    info = {'article': content,
            'author_name': author.username,
}
    return render_template('detail.html',**info)




# @app.route('/login/', methods=['GET','POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#     else:
#         username = request.form.get('username')
#         password = request.form.get('password')
#         g.username = username
#         login_log()
#         return "username:{},\n password:{}".format(username, password)

if __name__ == '__main__':
    ''' 如果入口程寻'''
    app.run(debug=True)