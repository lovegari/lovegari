# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import (
	StringField,
	PasswordField,
	TextAreaField
)
from wtforms import validators
from wtforms.fields.html5 import EmailField #말풍선 추가


class ArticleForm(Form):
	title = StringField(
		u'제목',
		[validators.data_required(u'제목을 입력하시기 바랍니다.')],
		description={'placeholder': u'Subject'}
	)
	content = TextAreaField(
		u'내용',
		[validators.data_required(u'내용을 입력하시기 바랍니다.')],
		description={'placeholder': u'Contents'}
	)
	author = StringField(
		u'작성자',
		[validators.data_required(u'이름을 입력하시기 바랍니다.')],
		description={'placeholder': u'Name'}
	)
	category = StringField(
		u'카테고리',
		[validators.data_required(u'카테고리를 입력하시기 바랍니다.')],
		description={'placeholder': u'Category'}
	)

class CommentForm(Form):
	content = StringField(
		u'내용',
		[validators.data_required(u'내용을 입력하시기 바랍니다.')],
		description={'placeholder': u'Contents'}
	)
	author = StringField(
		u'작성자',
		[validators.data_required(u'이름을 입력하시기 바랍니다.')],
		description={'placeholder': u'Name'}
	)
	password = PasswordField(
		u'비밀번호',
		[validators.data_required(u'비밀번호를 입력하시기 바랍니다.')],
		description={'placeholder': u'Password'}
	)
	email = EmailField(
		u'이메일',
		[validators.data_required(u'이메일을 입력하시기 바랍니다.')],
		description={'placeholder': u'Email'}
	)


class JoinForm(Form):
	email = EmailField(
		u'',
		[validators.data_required(u'이메일을 입력하시기 바랍니다.'),
		validators.Email(u'이메일을 입력하시기 바랍니다.')],
		description={'placeholder': u'Email'}
	)
	password = PasswordField(
		u'',
		[validators.data_required(u'비밀번호를 입력하시기 바랍니다.'),
		validators.EqualTo('confirm_password', message=u'비밀번호가 일치하지 않습니다.'),
		validators.Length(min=6, max=12, message=u'비밀번호는 6~12자리입니다.')],
		description={'placeholder': u'Password'}
	)
	confirm_password = PasswordField(
		u'',
		[validators.data_required(u'패스워드를 한번 더 입력하세요.')],
		description={'placeholder': u'Confirm password'}
	)
	name = StringField(
		u'',
		[validators.data_required(u'이름을 입력하시기 바랍니다.')],
		description={'placeholder': u'Name'}
	)
	
class LoginForm(Form):
	email = EmailField(
		'',
		[validators.data_required(u'이메일을 입력하시기 바랍니다.'),
		validators.Email(u'이메일을 입력하시기 바랍니다.')],
		description={'placeholder': u'Email'}
	)
	password = PasswordField(
		'',
		[validators.data_required(u'비밀번호를 입력하시기 바랍니다.')],
		description={'placeholder': u'Password'}
	)