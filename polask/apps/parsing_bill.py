#-*- coding: utf-8 -*-
# json 파싱하기

import urllib
import json

htmltext = urllib.urlopen("http://api.popong.com/v0.1/bill/?api_key=test&sort=proposed_date&order=desc")

data = json.load(htmltext)

# print data
# print

# data_print = json.dumps(data, sort_keys=True, indent=4)
# print data_print	# 단순 보기 좋게 출력하기 위함
# print

items = data['items']

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
	print
	print

