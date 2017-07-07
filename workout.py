import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


def load_exercise_data():		
	import csv		
 	with open('exercises.csv') as csvfile:		
		reader = csv.DictReader(csvfile)
		for row in reader:		
			if row['day_of_week'] == 'Monday':
				session.attributes['exercises'].append(row)
	return

@ask.launch
def launch():
	start_session()

	msg = render_template('welcome')+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).reprompt(render_template('exercise_options'))

def start_session():
	session.attributes['exercise_no'] = 0
	session.attributes['exercises'] = []
	load_exercise_data()
	session.attributes['exercise_total'] = len(session.attributes['exercises'])
	return	

def next():
	session.attributes['exercise_no'] = session.attributes['exercise_no'] + 1

	if session.attributes['exercise_no'] > session.attributes['exercise_total']:
		return False
	
	return True


def exercise_message():
	exercise_no = session.attributes['exercise_no'] - 1
	template_name = session.attributes['exercises'][exercise_no]['template_name']
	msg = ' '+render_template(template_name)
	return msg
	

@ask.intent("ReadyIntent")
def ready(phrase):
	acceptable_phrases = ['ready','yes','go','next','OK','skip']
	if (phrase not in acceptable_phrases):
		msg = render_template('misunderstand')+' '+render_template('exercise_options')
		msg = '<speak>'+msg+'</speak>'
		return question(msg).reprompt(render_template('continue_prompt'))

	exercise_no = session.attributes['exercise_no']
	msg = ''

	if (next() == False):
		msg = msg+' '+render_template('done')
		msg = '<speak>'+msg+'</speak>'
		return statement(msg)

	msg = msg+exercise_message()+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).reprompt(render_template('exercise_options'))


@ask.intent("GoDirectlyIntent")
def godirectly(exercise_no):
	start_session()

	if (exercise_no is None):
		msg = render_template('misunderstand')+' '+render_template('continue_prompt')
		msg = '<speak>'+msg+'</speak>'
		return question(msg).reprompt(render_template('exercise_options'))

	if (exercise_no.isdigit() == False):
		msg = render_template('misunderstand')+' '+render_template('continue_prompt')
		msg = '<speak>'+msg+'</speak>'
		return question(msg).reprompt(render_template('exercise_options'))

	if (int(exercise_no) < 1 or int(exercise_no) > session.attributes['exercise_total']):
		msg = render_template('misunderstand')+' '+render_template('continue_prompt')
		msg = '<speak>'+msg+'</speak>'
		return question(msg).reprompt(render_template('exercise_options'))

	session.attributes['exercise_no'] = int(exercise_no) - 1
	msg = ''

	if (next() == False):
		msg = msg+' '+render_template('done')
		msg = '<speak>'+msg+'</speak>'
		return statement(msg)

	msg = msg+exercise_message()+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).reprompt(render_template('exercise_options'))


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement(render_template('stop'))


@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement(render_template('stop'))


@ask.intent("AMAZON.HelpIntent")
def help():
	msg = render_template('help')+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).reprompt(render_template('exercise_options'))

# @ask.session_ended
# def session_ended():
# 	log.debug('Session Ended')
# 	return '', 200


if __name__ == '__main__':

    app.run(debug=True)
