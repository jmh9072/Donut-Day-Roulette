from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, send_file
from flask import abort
from database import db_session

import os
import datetime
import random

API_KEY = '12345'

MESSAGES_OF_THE_DAY = ['Free* donuts!',
                       'Eleven donuts are free. One costs eleven times too much.',
                       'Which one is the losing pastry?',
                       'Take a free donut, maybe?',
                       'What are you waiting for?',
                       'These donut have the ability to eat themselves!',
                       'Donut miss your chance!']
TOTAL_NUMBER_OF_DONUTS = 12

participants = {}
losing_participant = {}
app = Flask(__name__)

def render_template_page(filename, **kwargs):
    return render_template(filename, message_of_the_day=random.choice(MESSAGES_OF_THE_DAY), logged_in=False, **kwargs)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg']

@app.route('/')
def root():
    today = datetime.date.today()
    return render_template_page('index.html', participants=participants.get(today, []))

@app.route('/how_it_works')
def how_it_works():
    return render_template_page('how_it_works.html')

@app.route('/view_entries')
def view_entries():
    today = datetime.date.today()
    todays_participants = participants.get(today, [])
    todays_participant_list = []
    if len(todays_participants):
        todays_participant_list = todays_participants + (TOTAL_NUMBER_OF_DONUTS-len(todays_participants))*['']
    today = datetime.date.today()
    countdown_end_datetime = datetime.datetime(today.year, today.month, today.day, 17, 00, 00)
    if not today in losing_participant and datetime.datetime.now() > countdown_end_datetime:
        losing_participant[today] = random.choice(participants.get(today, ['Nobody']))
    return render_template_page('view_entries.html',
                                participants=todays_participant_list,
                                countdown_end_datetime=countdown_end_datetime.strftime('%b %d %Y %H:%M:%S'),
                                losing_participant=losing_participant.get(today, ''))

@app.route('/take_donut', methods=['POST', 'GET'])
def take_donut():
    today = datetime.date.today()
    todays_participants = participants.get(today, [])
    if request.method == 'POST':
        if len(todays_participants) < TOTAL_NUMBER_OF_DONUTS:
            name = request.form['name']
            if name:
                todays_participants.append(name)
                participants[today] = todays_participants
        return redirect(url_for('view_entries'))
    elif request.method == 'GET':
        number_of_donuts_remaining = 0
        countdown_end_datetime = datetime.datetime(today.year, today.month, today.day, 17, 00, 00)
        if datetime.datetime.now() <= countdown_end_datetime:
            number_of_donuts_remaining = TOTAL_NUMBER_OF_DONUTS-len(todays_participants)
        return render_template_page('take_donut.html', number_of_donuts_remaining=number_of_donuts_remaining)

@app.route('/donut_cam')
def donut_cam():
    today = datetime.date.today()
    todays_participants = participants.get(today, [])
    number_of_donuts_remaining = 0
    countdown_end_datetime = datetime.datetime(today.year, today.month, today.day, 17, 00, 00)
    if datetime.datetime.now() <= countdown_end_datetime:
        number_of_donuts_remaining = TOTAL_NUMBER_OF_DONUTS - len(todays_participants)
    return render_template_page('donut_cam.html', number_of_donuts_remaining=number_of_donuts_remaining)

@app.route('/upload_donut_cam_image', methods=['POST'])
def upload_file():
    # authentication check
    if not 'api-key' in request.form:
        abort(401)
    if request.form['api-key'] != API_KEY:
        abort(401)
    if not 'file' in request.files:
        abort(400)
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = 'donut_cam.jpg'
        file.save(os.path.join(os.getcwd(), 'static', filename))
        return 'Upload complete!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass

@app.route('/logout')
def logout():
    pass

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()