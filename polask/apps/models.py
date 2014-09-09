"""
models.py

"""

from apps import db

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255))
	password = db.Column(db.String(255))
	name = db.Column(db.String(255))
	join_date = db.Column(db.DateTime())

class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text())
	author = db.Column(db.String(255))
	category = db.Column(db.String(255))
	like = db.Column(db.Integer, default=0)
	date_created = db.Column(db.DateTime())

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
	article = db.relationship('Article',
							  backref=db.backref('comments', cascade='all, delete-orphan', lazy='dynamic'))

	author = db.Column(db.String(255))
	email = db.Column(db.String(255))
	password = db.Column(db.String(255))
	content = db.Column(db.Text())
	like = db.Column(db.Integer, default=0)
	date_created = db.Column(db.DateTime())

class Bill(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	proposed_date = db.Column(db.DateTime())
	decision_date = db.Column(db.DateTime())
	name = db.Column(db.String(100))
	assembly_id = db.Column(db.Integer)
	status_id = db.Column(db.Integer)
	status = db.Column(db.String(100))
	summary = db.Column(db.String(1000))
	sponsor = db.Column(db.String(100))
	status_ids = db.Column(db.Integer)
	document_url = db.Column(db.String(255))
	link_id = db.Column(db.Integer)
	is_processed = db.Column(db.Boolean)
	like = db.Column(db.Integer, default=0)

class Person(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	wiki = db.Column(db.String(255))
	name = db.Column(db.String(100))
	twitter = db.Column(db.String(255))
	gender = db.Column(db.String(100))
	image = db.Column(db.String(255))
	name_cn = db.Column(db.String(100))
	blog = db.Column(db.String(255))
	birthday = db.Column(db.DateTime())
	facebook = db.Column(db.String(255))
	address = db.Column(db.String(255))
	name_en = db.Column(db.String(100))
	education = db.Column(db.String(255))
	homepage = db.Column(db.String(255))
	education_id = db.Column(db.String(255))
	like = db.Column(db.Integer, default=0)