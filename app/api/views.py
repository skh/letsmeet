from . import api

@api.route('/parsemail')
def parsemail():
    return '{"content": "yeah!"}'