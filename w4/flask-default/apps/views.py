from flask import render_template, Flask
#from apps import app
import urllib
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route('/')
@app.route('/index')

def index():
	htmltext = urllib.urlopen("http://www.instiz.net/bbs/list.php?id=music&k=%5BMV%5D&stype=1").read()

	soup = BeautifulSoup(htmltext, from_encoding="utf-8")

	authors = []

	for item in soup.select(".listsubject"):
	   authors.append(item.get_text())

	"""
	for author in authors:
	print author.encode('utf-8')

	age = 21
	species = "Lion"
	friend = ["google","teacher","student"]
	"""

	return render_template("index.html",authors=authors)

if __name__ == "__main__":
	app.run(port=5005)