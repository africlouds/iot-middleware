from flask import Flask, request, flash, url_for, redirect, render_template
from flask.ext.jsonpify import jsonify
from flask_sqlalchemy import SQLAlchemy
import flask.ext.httpauth
import os
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///preferences.sqlite3'
app.config['SECRET_KEY'] = "random string"
auth = flask.ext.httpauth.HTTPBasicAuth()
db = SQLAlchemy(app)

users = {
    "admin": "admin"
}
GATEWAY = os.environ['GATEWAY']


@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

class Preference(db.Model):
   id = db.Column('preferebce_id', db.Integer, primary_key = True)
   user = db.Column(db.String(100))
   temperature = db.Column(db.String(50))

   def __init__(self, user, temperature):
   	self.user = user
	self.temperature = temperature

def get_preference(user):
	return Preference.query.filter_by(user = user).first()

@app.route('/preference', methods = ['POST'])
@app.route('/preference/<string:user>', methods = ['GET', 'PUT'])
@auth.login_required
def manage_preferences(user=None):
	if request.method == 'POST':
		preference = request.get_json(force=True)
		pref = get_preference(preference['user']) 
		code = None
		if pref:
			pref.temperature = preference['temperature']
			code = 200
		else:
			preference = Preference(preference['user'], preference['temperature'])
			db.session.add(preference)
			code = 201
         	db.session.commit()
		return "", code 
	elif request.method == 'GET' and user:
		pref = get_preference(user) 
		if not pref: 
			return "Not found", 404
		return jsonify({'user':pref.user,'temperature':pref.temperature})

@app.route('/reading')
@auth.login_required
def get_readings():
	return jsonify(requests.get(GATEWAY+'/reading', auth=('admin', 'admin')).json())
		


@app.route('/')
@auth.login_required
def welcome():
    return 'Smart Classroom Project'

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True,host='0.0.0.0')
