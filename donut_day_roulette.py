from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
import random

MESSAGES_OF_THE_DAY = ['Free* donuts!',
                       'Eleven donuts are free. One costs eleven times too much.',
                       'Which one is the losing pastry?',
                       'Take a free donut, maybe?',
                       'What are you waiting for?',
                       'These donut have the ability to eat themselves!',
                       'Donut miss your chance!']
TOTAL_NUMBER_OF_DONUTS = 12

participants = []
app = Flask(__name__)

def render_template_page(filename, **kwargs):
    return render_template(filename, message_of_the_day=random.choice(MESSAGES_OF_THE_DAY), **kwargs)

@app.route('/')
def root():
    return render_template_page('index.html', participants=participants)

@app.route('/how_it_works')
def how_it_works():
    return render_template_page('how_it_works.html')

@app.route('/view_entries')
def view_entries():
    participant_list = []
    if len(participants):
        participant_list = participants + (TOTAL_NUMBER_OF_DONUTS-len(participants))*['']
    return render_template_page('view_entries.html', participants=participant_list)

@app.route('/take_donut')
def take_donut():
    return render_template_page('take_donut.html', number_of_donuts_remaining=TOTAL_NUMBER_OF_DONUTS-len(participants))

@app.route('/donut_cam')
def donut_cam():
    return render_template_page('donut_cam.html', number_of_donuts_remaining=TOTAL_NUMBER_OF_DONUTS-len(participants))

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            participants.append(name)
    return redirect(url_for('view_entries'))
