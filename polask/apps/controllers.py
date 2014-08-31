# -*- coding: utf-8 -*-
from kstime import kstime
from flask import render_template, request, redirect, url_for, flash, g, session, jsonify
from werkzeug.security import generate_password_hash, \
	 check_password_hash #암호를 암호화한다
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from apps import app, db
from random import randint

import urllib
import json

from apps.forms import ArticleForm, CommentForm, JoinForm, LoginForm
from apps.models import (
	Article,
	Comment,
	User,
	Bill,
	Person
)

#
#@before request
#
@app.before_request #요청 전 검사 무조건!
def before_request():
	g.user_name = None

	if 'user_id' in session:
		g.user_name = session['user_name']
		g.user_email = session['user_email']
		g.user_id = session['user_id']

#
# @index & article list
#

@app.route('/', methods=['GET', 'POST'])
def frontgate():
	form = LoginForm()

	if request.method == 'POST':
	   if form.validate_on_submit():
			email = form.email.data
			password = form.password.data

			try: 
				user = db.session.query(User).filter(User.email==email).one() 
				if not check_password_hash(user.password, password): 
					flash(u'이메일 혹은 비밀번호를 확인해주세요.', 'danger') 
					return render_template('frontgate.html', form=form, active_tab='log_in') 
				else: 
					session.permanent = True 
					session['user_email'] = user.email 
					session['user_name'] = user.name 
					session['user_id'] = user.id

					flash(u'로그인 되었습니다.', 'success')
					return redirect(url_for('article_list')) 

			except NoResultFound, e: 
				flash(u'이메일 혹은 비밀번호를 확인해주세요.', 'danger') 
				return render_template('frontgate.html', form=form, active_tab='log_in') 

	#if GET
	return render_template('frontgate.html', form = form, active_tab='log_in')

@app.route('/list', methods=['GET'])
def article_list():
	context = {}
	context['article_list'] = Article.query.order_by(desc(Article.date_created)).all()
   
	return render_template("home.html", context=context, active_tab='timeline')

@app.route('/article/create', methods=['GET', 'POST'])
def article_create():
	form = ArticleForm()
	if request.method == 'POST':
		if form.validate_on_submit():

			article = Article(
				title = form.title.data,
				author = form.author.data,
				category = form.category.data,
				content = form.content.data,
				date_created = kstime(9)
			)

			db.session.add(article)
			db.session.commit()

			flash(u'게시글이 작성되었습니다.', 'success')
			return redirect(url_for('article_list'))
			
	return render_template('article/create.html', form=form, active_tab='article_create')

@app.route('/article/detail/<int:id>', methods=['GET'])
def article_detail(id):
	article = Article.query.get(id)
	comments = article.comments.order_by(desc(Comment.date_created)).filter_by(article_id=article.id)
	
	return render_template('article/detail.html', article=article, comments=comments)

@app.route('/article/update/<int:id>', methods=['GET', 'POST'])
def article_update(id):
	article = Article.query.get(id)
	form = ArticleForm(request.form, obj=article)
	if request.method == 'POST':
		if form.validate_on_submit():
			form.populate_obj(article)
			db.session.commit()
		return redirect(url_for('article_detail', id=id))

	return render_template('article/update.html', form=form)

@app.route('/article/delete/<int:id>', methods=['GET', 'POST'])
def article_delete(id):
	if request.method == 'GET':
		return render_template('article/delete.html', article_id=id)
	elif request.method == 'POST':
		article_id = request.form['article_id'] #맞았을지 모르겠다.
		article = Article.query.get(article_id)
		db.session.delete(article)
		db.session.commit()

		flash(u'게시글을 삭제하였습니다.', 'success')
		return redirect(url_for('article_list'))

@app.route('/article/detail_like', methods=['GET'])
def article_like_ajax():
	id = request.args.get('id',0,type=int)

	article = Article.query.get(id)
	article.like += 1

	db.session.commit()

	return jsonify(id=id)
#
# @comment controllers
#
@app.route('/comment/create/<int:article_id>', methods=['GET', 'POST'])
def comment_create(article_id):
	form = CommentForm()
	if request.method == 'POST':
		if form.validate_on_submit():
			comment = Comment(
				author=form.author.data,
				email=form.email.data,
				content=form.content.data,
				password=form.password.data,
				date_created = kstime(9),
				article=Article.query.get(article_id)
			)

			db.session.add(comment)
			db.session.commit()

			flash(u'댓글을 작성하였습니다.', 'success')
		return redirect(url_for('article_detail', id=article_id))
	return render_template('comment/create.html', form=form)

@app.route('/comment/delete/<int:id>', methods=['GET', 'POST'])
def comment_delete(id):
	if request.method == 'POST':
		comment = Comment.query.get(request.form['comment_id'])

		if request.form['password'] == comment.password:
			article_id = comment.article_id
			db.session.delete(comment)
			db.session.commit()

			flash(u'댓글을 삭제하였습니다.', 'success')
			return redirect(url_for('article_detail', id=article_id))
		else:
			flash(u'비밀번호가 틀렸습니다.', 'danger')
			return render_template('comment/delete.html', comment_id=request.form['comment_id'])

	elif request.method == 'GET':
		flash(u'경고! 댓글이 완전히 삭제되니, 다시 한번 확인하시기 바랍니다.', 'warning')
		return render_template('comment/delete.html', comment_id=id)

@app.route('/comment/detail_like', methods=['GET'])
def comment_like_ajax():
	id = request.args.get('id',0,type=int)

	comment = Comment.query.get(id)
	comment.like += 1

	db.session.commit()

	return jsonify(id=id)

#
# @Join controllers
#
@app.route('/user/join/', methods=['GET', 'POST'])
def user_join():
	form = JoinForm()

	if request.method == 'POST':
		if form.validate_on_submit():
			user = User(
				email=form.email.data,
				password=generate_password_hash(form.password.data),
				name=form.name.data,
				join_date = kstime(9)
			)

			db.session.add(user)
			db.session.commit()

			flash(u'가입이 완료 되었습니다.', 'success')
			return redirect(url_for('article_list'))
	#if GET
	return render_template('user/join.html', form=form, active_tab='user_join')

#
# @Login controllers
#
@app.route('/login', methods=['GET','POST'])
def log_in():
	form = LoginForm()

	if request.method == 'POST':
	   if form.validate_on_submit():
			email = form.email.data
			password = form.password.data

			try: 
				user = db.session.query(User).filter(User.email==email).one() 
				if not check_password_hash(user.password, password): 
					flash(u'이메일 혹은 비밀번호를 확인해주세요.', 'danger') 
					return render_template('user/login.html', form=form, active_tab='log_in') 
				else: 
					session.permanent = True 
					session['user_email'] = user.email 
					session['user_name'] = user.name 
					session['user_id'] = user.id

					flash(u'로그인 되었습니다.', 'success')
					return redirect(url_for('article_list')) 
			except NoResultFound, e: 
				flash(u'이메일 혹은 비밀번호를 확인해주세요.', 'danger') 
				return render_template('user/login.html', form=form, active_tab='log_in') 

	return render_template('user/login.html', form = form, active_tab='log_in')

@app.route('/logout')
def log_out():
	session.clear()

	return redirect(url_for('frontgate'))

@app.route('/bill/list')
def bill_list():
	htmltext = urllib.urlopen("http://api.popong.com/v0.1/bill/?api_key=test&sort=proposed_date&order=desc&per_page=20")
	data = json.load(htmltext)

	items = data['items']
	context = {}

	for number in range(len(items)):
		items = data['items'][number]
		context[number] = items

		try:
			bill = Bill (
				bill_id = context[number]['id']
			)

			db.session.add(bill)
			db.session.commit()

		except:
			pass
			
	return render_template("bill/list.html", context=context, bill=bill)

@app.route('/bill/detail/<int:id>', methods=['GET'])
def bill_detail(id):
	htmltext = urllib.urlopen("http://api.popong.com/v0.1/bill/"+ str(id) +"?api_key=test")
	bill = json.load(htmltext)
	
	return render_template('bill/detail.html', bill=bill)

@app.route('/bill/detail_like', methods=['GET'])
def bill_like_ajax():
	id = request.args.get('id',0,type=int)

	bill = Bill.query.get(id)
	bill.like += 1

	db.session.commit()

	return jsonify(id=id)

@app.route('/bill/timeline', methods=['GET'])
def bill_timeline():
	
	return render_template('bill/timeline.html')

@app.route('/person/list')
def person_list():
	htmltext = urllib.urlopen("http://api.popong.com/v0.1/person/?api_key=test&sort=image&order=desc&per_page=9")
	data = json.load(htmltext)

	items = data['items']
	context = {}

	for number in range(len(items)):
		items = data['items'][number]
		context[number] = items

		try:
			person = Person (
				person_id = context[number]['id']
			)

			db.session.add(person)
			db.session.commit()

		except:
			pass

	return render_template("person/list.html", context=context, person=person)

@app.route('/person/detail_like', methods=['GET'])
def person_like_ajax():
	id = request.args.get('id',0,type=int)

	person = Person.query.get(id)
	person.like += 1

	db.session.commit()

	return jsonify(id=id)

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