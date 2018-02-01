#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, render_template, request, g, session
import config
from exts import db
from models import Users, Articles, Comments
from sqlalchemy import or_
from hashx import encrypt
import os

app = Flask(__name__)
# 导入配置文件config.py
app.config.from_object(config)
#  注册db到app
db.init_app(app)
# 需要上下文处理器才能创建数据表
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    page_id = 1
    page_id = request.args.get('page_id')
    if session.get('user_id'):
        users = g.user
        content = {
            'questions': users.article,
            'author': users
        }
        return render_template('indext.html', **content)
    else:
        articles = Articles.query.all()
        article_num = len(articles)
        page = int(article_num/5)
        if page >= 1 and article_num % 5 == 0:
            pages = page
        elif page >= 1 and article_num % 5 != 0:
            pages = page+1
        else:
            pages = 1
        pages_list = range(1, pages+1)
        page_id = request.args.get('page_id')
        if page_id:
            page_slice = slice(0+5*(int(page_id)-1), 5+5*(int(page_id)-1))
            questions = articles[page_slice]
        else:
            questions = articles[slice(0,5)]
        content = {
                'questions': questions,
                'article_nums': article_num,
                'pages_list': pages_list,
            }
        return render_template('indext.html', **content)


# @app.before_request
# def my_befor_request():
#     print('hello,nihao')

# 登陆页面视图函数
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login2.html')
    else:
        tellphone = request.form.get('tel')
        password1 = request.form.get('password1')
        password = encrypt(password1)
        user = Users.query.filter_by(tel=tellphone, password1=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return "登陆用户或者密码输入错误，请重新输入"


# 查询页面
@app.route('/my_blog/')
def my_blog():
    q = request.args.get('q')
    # articles = Articles.query.filter(Articles.title.ilike('%{}%'.format(q)))
    articles = Articles.query.filter(or_(Articles.content.contains(q),
                                         Articles.title.contains(q)))
    content = {
        'questions': articles
    }
    return render_template('indext.html', **content)


# 钩子函数（hook) context_processor 装饰器，返回字典，所有页面都可用
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    user = Users.query.filter_by(id=user_id).first()
    g.user = user
    return


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = g.user
        return {'user': user}
    else:
        return {}


# 注册视图函数
@app.route('/register/', methods=['GET', 'POST'])
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
            password = encrypt(password1)
            user = Users(username=name, tel=tel, password1=password)
            db.session.add(user)
            db.session.commit()
            return '注册成功'


# 文章发布视图函数

@app.route('/article/', methods=['GET', 'POST'])
def article():
    if request.method == 'GET':
        return render_template('article.html')
    else:
        a_id = session.get('user_id')
        a_title = request.form.get('theme')
        a_content = request.form.get('content')
        articles = Articles(author_id=a_id, title=a_title, content=a_content)
        db.session.add(articles)
        db.session.commit()
        return '发布成功'


# 注销
@app.route('/login_out/')
def login_out():
    # session.pop('user_id')
    del session['user_id']
    session.clear()
    print(session.get('user_id'))
    return redirect(url_for('register'))


# 笔记详情页面
@app.route('/detail/<question_id>', methods=['GET', 'POST'])
def detail(question_id):
    if request.method == 'GET':
        content = Articles.query.filter_by(id=question_id).first()
        author = Users.query.filter_by(id=content.author_id).first()
        info = {'article': content,
                'author_name': author.username,
                'comments': content.comment,
                'comments_count': len(content.comment)
                }

        return render_template('detail.html', **info)
    elif session.get('user_id'):
        comment = request.form.get('comment')
        comments = Comments(comment=comment, articles_id=question_id, author_id=session.get('user_id'))
        db.session.add(comments)
        db.session.commit()
        return redirect(url_for('detail', question_id=question_id))
    return redirect(url_for('login'))


@app.route('/pyecharts/')
def echarts():
    from pyechrts import myecharts
    chart = myecharts()
    return render_template('pyecharts.html', myechart=chart)


if __name__ == '__main__':
    # 如果入口程序为主程序
    app.run(debug=True)
