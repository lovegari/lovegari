#-*- coding: utf-8 -*-
# json 파싱하기

import urllib
import json

htmltext = urllib.urlopen("http://api.popong.com/v0.1/person/?api_key=test")

data = json.load(htmltext)

# print data
# print

# data_print = json.dumps(data, sort_keys=True, indent=4)
# print data_print	# 단순 보기 좋게 출력하기 위함
# print

items = data['items']

for number in range(len(items)):
	items = data['items'][number]

	wiki = items['wiki']
	address_id = items['address_id']
	name = items['name']
	twitter = items['twitter']
	gender = items['gender']
	image = items['image']
	name_cn = items['name_cn']
	blog = items['blog']
	birthday = items['birthday']
	address = items['address']
	name_en = items['name_en']
	education = items['education']
	homepage = items['homepage']
	id = items['id']
	education_id = items['education_id']

	print wiki
	print address_id
	print name
	print twitter
	print gender
	print image
	print name_cn
	print blog
	print birthday
	print address
	print name_en
	print education
	print homepage
	print id
	print education_id
	print
	print

