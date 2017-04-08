from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
import random
import datetime

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
    return render_template(filename, message_of_the_day=random.choice(MESSAGES_OF_THE_DAY), **kwargs)

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
    countdown_end_datetime = datetime.datetime(today.year, today.month, today.day, 17, 0, 0)
    if not countdown_end_datetime in losing_participant and datetime.datetime.now() > countdown_end_datetime:
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
        return render_template_page('take_donut.html', number_of_donuts_remaining=TOTAL_NUMBER_OF_DONUTS-len(todays_participants))

@app.route('/donut_cam')
def donut_cam():
    today = datetime.date.today()
    todays_participants = participants.get(today, [])
    return render_template_page('donut_cam.html', number_of_donuts_remaining=TOTAL_NUMBER_OF_DONUTS-len(todays_participants))
