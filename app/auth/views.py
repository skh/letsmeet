from flask import redirect, request, url_for, render_template
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User

'''
@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')
'''

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        missing = _validate(
            request.form,
            ['email', 'password'])
        if len(missing) > 0:
            return render_template('auth/login.html')
        user = db.session.query(User).filter_by(email=request.form['email']).one()
        if user is not None and user.verify_password(request.form['password']):
            login_user(user, True)
            return redirect(url_for('main.index'))
        else:
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        missing = _validate(
            request.form, 
            ['email', 'name', 'password', 'confirm_password'])
        # if not valid, show error
        if len(missing) > 0:
            # TODO: flash error message
            return render_template('auth/register.html')
        elif request.form['confirm_password'] != request.form['password']:
            # TODO: flash error message
            return render_template('auth/register.html')
        else:
            #create user and redirect
            user = User(email=request.form['email'],
                    name=request.form['name'],
                    password=request.form['password'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html')

def _validate(data, fields):
    missing = []
    for field in fields:
        if data[field] == "":
            missing.append(field)
    print missing
    return missing