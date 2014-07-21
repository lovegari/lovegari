from flask import render_template, Flask, request
#from apps import app

app = Flask(__name__)
@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
	get = None
	post = None
	
	if request.args:
		get = request.args['text_get']

	if request.form:
		post = request.form['text_post']

	return render_template("index.html", variable_get = get, variable_post = post)

if __name__ == "__main__":
	app.run(port = 5009)