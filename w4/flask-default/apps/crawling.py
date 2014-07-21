# -*- coding:utf-8 -*-
import urllib
from bs4 import BeautifulSoup
   

htmltext = urllib.urlopen("http://www.instiz.net/bbs/list.php?id=music&k=%5BMV%5D&stype=1").read()

soup = BeautifulSoup(htmltext, from_encoding="utf-8")

authors = []

for item in soup.select(".listsubject"):
   authors.append(item.get_text())

for author in authors:
   print author.encode('utf-8')