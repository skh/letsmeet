from flask import render_template, jsonify
from . import main
from .. import db
from ..models import User, Meeting


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/meetings', methods=['GET'])
def list_meetings():
    # if logged in etc.
    user = db.session.query(User).filter_by(id=1).one()
    return jsonify(Meetings=[m.serialize for m in user.meetings])

