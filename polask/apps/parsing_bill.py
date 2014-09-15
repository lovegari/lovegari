#-*- coding: utf-8 -*-
# json 파싱하기

import urllib
import json



# print data
# print

# data_print = json.dumps(data, sort_keys=True, indent=4)
# print data_print	# 단순 보기 좋게 출력하기 위함
# print



# htmltext = urllib.urlopen("http://api.popong.com/v0.1/bill/?api_key=test&sort=proposed_date&order=desc&per_page=20")

# data = json.load(htmltext)

# items = data['items']

# for number in range(len(items)):
# 	item = data['items'][number]

# 	id = item['id']
# 	name = item['name']
# 	assembly_id = item['assembly_id']
# 	status = item['status']
# 	proposed_date = item['proposed_date']
# 	sponsor = item['sponsor']
# 	status = item['status']
# 	status_id = item['status_id']
# 	status_ids = item['status_ids']
# 	summary = item['summary']
# 	document_url = item['document_url']
# 	decision_date = item['decision_date']
# 	link_id = item['link_id']
# 	if item['is_processed'] == True:
# 		is_processed = 1
# 	else:
# 		is_processed = 0


htmltext = urllib.urlopen('http://api.popong.com/v0.1/bill/?api_key=test&sort=proposed_date&order=desc&per_page=20')
data = json.load(htmltext)

items = data['items']

# for item in items:
# 	status = item['status'],
# 	proposed_date = item['proposed_date'],
# 	name = item['name'],
# 	assembly_id = item['assembly_id'],
# 	status_id = item['status_id'],
# 	summary = item['summary'],
# 	sponsor = item['sponsor'],
# 	status_ids = item['status_ids'],
# 	document_url = item['document_url'],
# 	decision_date = item['decision_date'],
# 	link_id = item['link_id'],
# 	is_processed = item['is_processed'],
# 	id = item['id']


for number in range(len(items)):
	items = data['items'][number]
	assembly_id = items['assembly_id']
	document_url = items['document_url']
	id = items['id']
	is_processed = items['is_processed']
	link_id = items['link_id']
	name = items['name']
	proposed_date = items['proposed_date']
	sponsor = items['sponsor']
	status = items['status']
	status_id = items['status_id']
	status_ids = items['status_ids']
	summary = items['summary']

	print assembly_id
	print document_url
	print id
	print is_processed
	print link_id
	print name
	print proposed_date
	print sponsor
	print status
	print status_id
	print status_ids
	print summary
	print is_processed
	print

# id = 1911469

# htmltext = urllib.urlopen("http://api.popong.com/v0.1/bill/"+ str(id) +"?api_key=test")
# bill = json.load(htmltext)

# print bill['name']


# htmltext = urllib.urlopen("http://api.popong.com/v0.1/bill/?api_key=test&status_id=12&order=asc&per_page=1000")

# data = json.load(htmltext)

# items = data['items']

# context = {}
# bill = {}

# print data
# print

# data_print = json.dumps(data, sort_keys=True, indent=4)
# print data_print	# 단순 보기 좋게 출력하기 위함
# print

# for number in range(len(items)):
# 	items = data['items'][number]
# 	context[number] = items

# if context:
# 	for number in range(len(context)):
# 		print context[number]['status']
# 		print context[number]['status_id']

# if context:
# 	for number in range(len(context)):
# 		print number
# 		print context[number]['id']
# 		print context[number]['assembly_id']
# 		print context[number]['name']
# 		print context[number]['sponsor']
# 		print context[number]['proposed_date']
# 		print context[number]['status']
# 		print context[number]['summary']
# 		print context[number]['is_processed']
# 		print context[number]['status_id']
