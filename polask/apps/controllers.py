# -*- coding: utf-8 -*-
from kstime import kstime
from flask import render_template, request, redirect, url_for, flash, g, session, jsonify
from werkzeug.security import generate_password_hash, \
	 check_password_hash #암호를 암호화한다
from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from apps import app, db
from bs4 import BeautifulSoup

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

@app.route('/db/update/person')
def update_person():
	htmltext = urllib.urlopen('http://api.popong.com/v0.1/person/?api_key=test&sort=image&order=desc&per_page=9&assembly_id=19')
	data = json.load(htmltext)

	items = data['items']

	for number in range(len(items)):
		item = data['items'][number]

		try:
			person = Person(
				id = item['id'],
				wiki = item['wiki'],
				name = item['name'],
				twitter = item['twitter'],
				gender = item['gender'],
				image = item['image'],
				name_cn = item['name_cn'],
				blog = item['blog'],
				birthday = item['birthday'],
				facebook = item['facebook'],
				address = item['address'],
				name_en = item['name_en'],
				homepage = item['homepage']
			)

			db.session.add(person)
			db.session.commit()

		except:
			pass

	return redirect(url_for('update_bill'))

# @app.route('/db/update/bill_person')
# def update_bill_person():
# 	htmltext = urllib.urlopen("http://pokr.kr/person/19601167").read()

# 	soup = BeautifulSoup(htmltext, from_encoding="utf-8")

# 	raw_bills = []
# 	bills = []

# 	for link in soup.select('#person-legislations td a'):
# 		raw_bills.append(link.get('href'))

# 	for num in raw_bills:
# 		if num.split("/")[1] == "bill":
# 			bills.append(int(num.split("/")[2]))

# 	contents = {}

# 	for num in bills:
# 		html = urllib.urlopen("http://api.popong.com/v0.1/bill/" + str(num) + "?api_key=test")
# 		data = json.load(html)
# 		contents[num] = data

# 		if contents[num]['is_processed'] == True:
# 			processed = 1
# 		else:
# 			processed = 0

# 		try:
# 			bill = Bill(
# 				id = contents[num]['id'],
# 				status = contents[num]['status'],
# 				proposed_date = contents[num]['proposed_date'],
# 				name = contents[num]['name'],
# 				assembly_id = contents[num]['assembly_id'],
# 				status_id = contents[num]['status_id'],
# 				summary = contents[num]['summary'],
# 				sponsor = contents[num]['sponsor'],
# 				# status_ids = contents[num]['status_ids'],
# 				document_url = contents[num]['document_url'],
# 				decision_date = contents[num]['decision_date'],
# 				link_id = contents[num]['link_id'],
# 				is_processed = processed
# 			)

# 			db.session.add(bill)
# 			db.session.commit()

# 		except:
# 			pass

# 	return redirect(url_for('update_bill'))

@app.route('/db/update/bill')
def update_bill():
	htmltext = urllib.urlopen('http://api.popong.com/v0.1/bill/?api_key=test&sort=proposed_date&order=desc&per_page=30')
	data = json.load(htmltext)

	items = data['items']

	for number in range(len(items)):
		item = data['items'][number]

		if item['is_processed'] == True:
			processed = 1
		else:
			processed = 0

		try:
			bill = Bill(
				id = item['id'],
				status = item['status'],
				proposed_date = item['proposed_date'],
				name = item['name'],
				assembly_id = item['assembly_id'],
				status_id = item['status_id'],
				summary = item['summary'],
				sponsor = item['sponsor'],
				# status_ids = item['status_ids'],
				document_url = item['document_url'],
				decision_date = item['decision_date'],
				link_id = item['link_id'],
				is_processed = processed
			)

			db.session.add(bill)
			db.session.commit()

		except:
			pass

	return redirect(url_for('article_list'))

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
					return redirect(url_for('update_person')) 

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

			return redirect(url_for('user_interest', user_id = user.id))
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

@app.route('/user/interest/<int:user_id>', methods=['GET','POST'])
def user_interest(user_id):
	# if request.method == 'POST':
	# 	flash(u'가입이 완료 되었습니다.', 'success')
	# 	return redirect(url_for('log_in'))

	return render_template('user/interest.html', user_id = user_id)

@app.route('/user/set_interest', methods=['POST'])
def set_interest():
	data = request.form
	user_id = data['user_id']
	interests = data['s_list']

	user = User.query.get(user_id)

	for item in interests[1:-1].split(","):
		interest = item[1:-1]
		if interest == "law":
			user.law = 10
		elif interest == "finance":
			user.finance = 10
		elif interest == "defense":
			user.defense = 10
		elif interest == "budget":
			user.budget = 10
		elif interest == "ethics":
			user.ethics = 10
		elif interest == ("deploy" or "unite"):
			user.deploy = 10
		elif interest == ("safety" or "administer"):
			user.safety = 10
		elif interest == ("edu" or "culture" or "sports" or "sight"):
			user.edu = 10
		elif interest == ("science" or "communication" or "broadcast"):
			user.science = 10
		elif interest == ("agriculture" or "food" or "ocean"):
			user.agriculture = 10
		elif interest == ("industry" or "resource" or "startup"):
			user.industry = 10
		elif interest == ("health" or "welfare"):
			user.health = 10
		elif interest == ("environment" or "labor"):
			user.environment = 10
		elif interest == ("country" or "transportation"):
			user.country = 10
		elif interest == ("family" or "female"):
			user.family = 10


	db.session.commit()

	return jsonify(status = 0)



@app.route('/logout')
def log_out():
	session.clear()

	return redirect(url_for('frontgate'))

@app.route('/bill/list')
def bill_list():
	context = {}
	context['bill_list'] = Bill.query.order_by(desc(Bill.proposed_date)).all()
	 
	return render_template("bill/list.html", context=context)

@app.route('/bill/<int:id>', methods=['GET'])
def bill_detail(id):
	bill = Bill.query.get(id)
	
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
	context = {}
	context['person_list'] = Person.query.order_by(desc(Person.birthday)).all()

	return render_template("person/list.html", context=context)

@app.route('/person/detail_like', methods=['GET'])
def person_like_ajax():
	id = request.args.get('id',0,type=int)

	person = Person.query.get(id)
	person.like += 1

	db.session.commit()

	return jsonify(id=id)

@app.route('/person/<int:id>', methods=['GET'])
def person_detail(id):
	person = Person.query.get(id)
	
	htmltext = urllib.urlopen("http://pokr.kr/person/"+str(person.id)).read()

	soup = BeautifulSoup(htmltext)

	raw_bills = []
	bills = []

	for link in soup.select('#person-legislations td a'):
		raw_bills.append(link.get('href'))

	for num in raw_bills:
		if num.split("/")[1] == "bill":
			bills.append(int(num.split("/")[2]))

	contents = []

	for num in bills:
		htmltext = urllib.urlopen("http://api.popong.com/v0.1/bill/" + str(num) + "?api_key=test&sort=proposed_date&order=desc")
		data = json.load(htmltext)
		contents.append(data)

		if data['is_processed'] == True:
			processed = 1
		else:
			processed = 0

		try:
			bill = Bill(
				id = data['id'],
				status = data['status'],
				proposed_date = data['proposed_date'],
				name = data['name'],
				assembly_id = data['assembly_id'],
				status_id = data['status_id'],
				summary = data['summary'],
				sponsor = data['sponsor'],
				# status_ids = data['status_ids'],
				document_url = data['document_url'],
				decision_date = data['decision_date'],
				link_id = data['link_id'],
				is_processed = processed
			)

			db.session.add(bill)
			db.session.commit()

		except:
			db.session.rollback()
			pass

	return render_template('person/detail.html', person=person, contents=contents)

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