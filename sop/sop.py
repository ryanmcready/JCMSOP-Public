from flask import Flask, render_template, request, make_response, session, redirect, url_for, flash
from markupsafe import escape
import requests
import json


app = Flask(__name__)
app.secret_key = ''

# Key required to "Log In" - Not secure for production.
ACCESS_KEY = 'jcm1'

# JCM Logo Colors
# 1 - Dark Blue:
	# Hex Code: #1f3c73
	# RGB: rgb(31, 60, 115)
# 2 - Grey:
	# Hex Code: #d0d2d3
	# RGB: rgb(208, 210, 211)

alert = None

def log_ln(log_text):
	print("LOG: " + log_text)

# Main Webpage - Table of Contents for SOP
@app.route('/', methods=['GET'])
def jcmhelp():
	# Temporary: Defining a current user
	session['user'] = 'JCM Test User'
	try:
		# If the user is not logged in, redirect to login page
		if session['logged_in'] == False:
			return redirect(url_for('login'))
		# If the user is logged in, redirect to /sop
		elif session['logged_in'] == True:
			return redirect(url_for('sop'))
		else:
			log_ln('Error checking login status')
			return redirect(url_for('errorpage'))
	# If 'logged_in' has not been defined in session, redirect to login page
	except:
		session['logged_in'] = False
		return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
	# If user is navigating (GET) to /login:
	if request.method == 'GET':
		try:
			# If user is not logged in, render the login form
			if session['logged_in'] == False:
				return render_template('login.html')
			elif session['logged_in'] == True:
				alert = 'You are already logged in. Visit https://jcm.help/logout to logout.'
				return redirect(url_for('jcmhelp', alert=alert))
			else:
				return redirect(url_for('errorpage'))
		except:
			return redirect(url_for('errorpage'))

	elif request.method == 'POST':
		if request.form['userFormKey'] == ACCESS_KEY:
			# If the Access Key is valid, log in.
			session['logged_in'] = True
			return redirect(url_for('jcmhelp'))

		elif request.form['userFormKey'] != ACCESS_KEY:
			# If the Access Key is invalid, re-render the login template and provide error
			session['logged_in'] = False
			flash("incorrect!")
			return redirect(url_for('login'))
		else:
			return 'error'


# Visit https://jcm.help to remove the user and logged_in status from the session
@app.route('/logout', methods=['GET'])
def logout():
	session.pop('logged_in', None)
	session.pop('user', None)
	log_ln('Session Popped.....')
	return redirect(url_for('login'))

@app.route('/sop')
def sop():
	return 'Temporary'

@app.route('/error')
def errorpage():
	return 'Temporary - Error Page'

