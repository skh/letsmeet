from flask import make_response, request
from . import api
from .. import db
from ..models import User, Meeting, Action, Topic

import json
from email.utils import parseaddr

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
            meeting = Meeting(title=subject, text=body_plain)
            meeting.users.append(uq.one())

            # get participant list from To: and Cc:
            participant_emails = _getparticipants(message_headers)

            for email in participant_emails:
                # only add registered users to meeting
                uq = db.session.query(User).filter_by(email=email)
                if uq.count() == 1:
                    meeting.users.append(uq.one())

            db.session.add(meeting)
            db.session.commit()

            # send email
    else:
        user = db.session.query(User).filter_by(id=1).one()
        meeting = Meeting(title="Meeting 1")
        meeting.users.append(user)
        db.session.add(meeting)
        db.session.commit()


    # Returned text is ignored but HTTP status code matters:
    # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
    return make_response('OK', 200)

def _parseheaders(header_json):
    result = {}
    # the header json string contains a list of lists with 2 members each
    for header in json.loads(header_json):
        result[header[0]] = header[1]
    return result

def _getparticipants(header_json):

    headers = _parseheaders(header_json)

    taboo = 'helper@sandbox196a545932dc4ad6ab58ea66895a5405.mailgun.org'
    emails = set()

    for recipient in headers['To'].split(','):
        address = parseaddr(recipient.strip())[1]
        if address != taboo:
            emails.add(address)

    if headers.has_key('Cc'):
        for recipient in headers['Cc'].split(','):
            address = parseaddr(recipient.strip())[1]
            if address != taboo:
                emails.add(address)

    return list(emails)