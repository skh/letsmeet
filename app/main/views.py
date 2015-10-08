from flask import render_template, jsonify
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
    return render_template('index.html')

@main.route('/meetinglist', methods=['GET'])
def list_meetings():
    # if logged in etc.
    if current_user.is_authenticated:
        return jsonify(Meetings=[m.serialize for m in current_user.meetings])
    else:
        return '{"boo": true}'

