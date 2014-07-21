from flask import render_template, Flask
from apps import app

#app = Flask(__name__)
@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

#if __name__ == "__main__":
#	app.run(port = 5007)