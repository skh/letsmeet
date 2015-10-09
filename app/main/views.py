from flask import render_template, jsonify, make_response
from flask.ext.login import current_user, login_required
from . import main
from .. import db, login_manager
from ..models import User, Meeting


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/meetings')
@login_required
def meetings():
    return render_template('meetings.html')

@main.route('/meetinglist', methods=['GET'])
def list_meetings():
    # if logged in etc.
    if current_user.is_authenticated:
        return jsonify(Meetings=[m.serialize for m in current_user.meetings])
    else:
        return '{"boo": true}'

@main.route('/meeting/<id>', methods=['POST'])
def update_meeting(id):
	meeting = db.session.query(Meeting).get(id)
	if meeting == None:
		return make_response('No such item', 404)
	if request.form.has_key('text'):
		meeting.text = request.form['text']
		db.session.add(meeting)
		db.session.commit()

	return make_response('OK', 200)



