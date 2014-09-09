#-*- coding: utf-8 -*-
# json 파싱하기

import urllib
import json

htmltext = urllib.urlopen("http://api.popong.com/v0.1/person/?api_key=test&sort=image&order=desc&per_page=10")

data = json.load(htmltext)

# print data
# print

# data_print = json.dumps(data, sort_keys=True, indent=4)
# print data_print	# 단순 보기 좋게 출력하기 위함
# print

items = data['items']

context = {}
people = {}

for number in range(len(items)):
	items = data['items'][number]
	context[number] = items

if context:
	for number in range(len(context)):
		print context[number]['twitter']
		print context[number]['blog']
		print context[number]['facebook']
		print context[number]['homepage']
		print context[number]['wiki']
		print