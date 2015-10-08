from flask import make_response, request
from . import api
from .. import db
from ..models import User, Meeting, Action, Topic

@api.route('/parsemail', methods=['POST','GET'])
def parsemail():
    # see https://documentation.mailgun.com/quickstart-receiving.html
    if request.method == 'POST':
        sender = request.form['sender']
        subject = request.form['subject']
        message_headers = request.form['message-headers']
        body_plain = request.form['body-plain']

        # sanitize subject: ignore 'Re: ' etc.
        # if subject already exists, do nothing

        # check if user exists
        uq = db.session.query(User).filter_by(email=sender)
        if uq.count() == 1:
            # create meeting
            meeting = Meeting(title=subject)
            meeting.users.append(uq.one())
            db.session.add(meeting)
            db.session.commit()

            # send email

        # get participant list from To:, From: and Cc:
        # for each participant:
          # if registered: send invite
          # if unconfirmed: do nothing
          # if unknown: create account, send confirmation mail, send invite
    else:
        user = db.session.query(User).filter_by(id=1).one()
        meeting = Meeting(title="Meeting 1")
        meeting.users.append(user)
        db.session.add(meeting)
        db.session.commit()


    # Returned text is ignored but HTTP status code matters:
    # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
    return make_response('OK', 200)