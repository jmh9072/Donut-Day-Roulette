from flask import Flask
app = Flask(__name__)

participants = []

from flask import render_template
from flask import request
from flask import redirect, url_for

@app.route('/')
def root():
	return render_template('index.html', participants=participants)
	
@app.route('/add', methods=['POST'])
def add():
	if request.method == 'POST':
		name = request.form['name']
		if name:
			participants.append(name)
	return redirect(url_for('root'))
	
