from flask import make_response
from . import api

@api.route('/parsemail', methods=['POST'])
def parsemail():
    # see https://documentation.mailgun.com/quickstart-receiving.html
    if request.method == 'POST':
        sender = request.form['sender']
        subject = request.form['subject']
        message_headers = request.form['message-headers']
        body_plain = request.form['body-plain']


    # Returned text is ignored but HTTP status code matters:
    # Mailgun wants to see 2xx, otherwise it will make another attempt in 5 minutes
    return make_response('OK', 200)