# -*- coding: utf-8 -*-
from kstime import kstime
from flask import render_template, request, flash, url_for, redirect
from sqlalchemy import desc
from apps import app, db

from apps.models import (
	Article,
	Comment,
	Login
)

@app.route('/', methods=['GET', 'POST'])
def frontgate():
	return render_template("frontgate.html")

@app.route('/login/create', methods=['GET', 'POST'])
def login_create():
	if request.method == 'GET':
		return render_template("login/create.html", active_tab = 'login_create')
	elif request.method == 'POST':
		login_data = request.form

		login = Login(
			login_pw = login_data['login_pw'],
			login_rpw = login_data['login_rpw'],
			login_name = login_data['login_name'],
			login_email = login_data['login_email'],
			date_created = kstime(9),
		)

		if login.login_pw == login.login_rpw:
			db.session.add(login)
			db.session.commit()

			flash(u'아이디가 성공적으로 만들어졌습니다.', 'success')
			return redirect(url_for('login_interest', login=login))

		else:
			flash(u'비밀번호를 다시 확인해주세요.', 'danger')
			return redirect(url_for('login_create', login=login))

@app.route('/login/interest', methods=['GET', 'POST'])
def login_interest():
	return render_template("login/interest.html")

@app.route('/list', methods=['GET'])
def article_list():
	context = {}
	context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()
   
	return render_template("home.html", context=context, active_tab='timeline')

@app.route('/article/create', methods=['GET', 'POST'])
def article_create():
	if request.method == 'GET':
		return render_template("article/create.html", active_tab = 'article_create')
	elif request.method == 'POST':
		article_data = request.form

		article = Article(
			title = article_data['title'],
			author = article_data['author'],
			category = article_data['category'],
			content = article_data['content'],
			password = article_data['password'],
			date_created = kstime(9),
			count = 0
		)

		db.session.add(article)
		db.session.commit()

		flash(u'게시글이 작성되었습니다.', 'success')

		return redirect(url_for('article_list'))

@app.route('/article/detail/<int:id>', methods=['GET', 'POST'])
def article_detail(id):
	article = Article.query.get(id)
	comments = article.comments.order_by(desc(Comment.date_created)).all()
	
	return render_template('article/detail.html', article=article, comments=comments)

@app.route('/article/like/<int:id>', methods=['GET', 'POST'])
def article_like(id):
	article = Article.query.get(id)
	article.count += 1

	db.session.commit()

	return redirect(url_for('article_detail', id=id))

@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
	article = Article.query.get(id)
	if request.method == 'GET':
		return render_template('article/update.html', article=article)
	elif request.method == 'POST':
		article_data = request.form

		article = Article.query.get(id)

		article.title = article_data['title']
		article.author = article_data['author']
		article.category = article_data['category']
		article.content = article_data['content']

		if article.password == article_data['password']:
			db.session.commit()
			flash(u'게시글이 수정되었습니다.', 'success')
			return redirect(url_for('article_detail', id=id))

		else:
			flash(u'비밀번호가 틀렸습니다.', 'danger')
			return redirect(url_for('article_update', id=id))

@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
	article = Article.query.get(id)

	if request.method == 'GET':
		return render_template('article/delete.html', article=article)
	elif request.method == 'POST':
		article_data = request.form

		article = Article.query.get(id)

		if article.password == article_data['password']:
			db.session.delete(article)
			db.session.commit()

			flash(u'게시글을 삭제하였습니다.', 'success')
			return redirect(url_for('article_list'))

		else:
			flash(u'비밀번호가 틀렸습니다.', 'danger')
			return redirect(url_for('article_delete', id=id))

#
# @comment controllers
#
@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    if request.method =='GET':
        return render_template('comment/create.html')
    elif request.method == 'POST':

        comment_data = request.form

        comment = Comment(
            
            author = comment_data['author'],
            email = comment_data['email'],
            content = comment_data['content'],
            password = comment_data['password'],
            article = Article.query.get(article_id),
            date_created = kstime(9),
            count = 0

        )

        db.session.add(comment)
        db.session.commit()

        flash(u'댓글을 작성하였습니다.', 'success')
        return redirect(url_for('article_detail', id=article_id))

@app.route('/comment/like/<int:id>', methods=['GET', 'POST'])
def comment_like(id):
	comment = Comment.query.get(id)
	comment.count += 1

	db.session.commit()

	id = comment.article_id

	return redirect(url_for('article_detail', id=id))

@app.route('/comment/delete/<int:id>', methods=['GET', 'POST'])
def comment_delete(id):
	comment = Comment.query.get(id)

	if request.method == 'GET':
		return render_template('comment/delete.html', comment=comment)
	elif request.method == 'POST':
		comment_data = request.form

		comment = Comment.query.get(id)

		if comment.password == comment_data['password']:
			db.session.delete(comment)
			db.session.commit()

			id = comment.article_id

			flash(u'댓글을 삭제하였습니다.', 'success')
			return redirect(url_for('article_detail', id=id))

		else:
			flash(u'비밀번호가 틀렸습니다.', 'danger')
			return redirect(url_for('comment_delete', id=id))
#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500