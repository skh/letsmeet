from flask import redirect, request, url_for, render_template, flash
from flask.ext.login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from ..email import send_email

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
            flash('Login unsuccessful.')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        missing = _validate(
            request.form, 
            ['email'])
        # if not valid, show error
        if len(missing) > 0:
            flash('Please enter your email address.')
            return render_template('auth/register.html')
        else:
            # email must be unique
            uq = db.session.query(User).filter_by(email=request.form['email'])
            if uq.count() > 0:
                flash('This email has already been registered.')
                return redirect(url_for('auth.register'))

            # create user and redirect
            user = User(email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            send_email(user.email, 'Confirm Your Account',
                'auth/email/confirm', user=user, token=token, email=user.email)
            flash('Success! Please check your inbox for the confirmation email.')
            return redirect(url_for('auth.login'))
    else:
        return render_template('auth/register.html')


@auth.route('/confirm/<token>/<email>', methods=['GET', 'POST'])
def confirm(token, email):
    if request.method == 'POST':
        missing = _validate(
            request.form,
            ['name', 'password', 'confirm_password'])

        if len(missing) > 0:
            flash('Please fill in all fields.')
            return render_template('auth/confirm.html', token=token, email=email)

        if request.form['password'] != request.form['confirm_password']:
            flash('Passwords must match.')
            return render_template('auth/confirm.html', token=token, email=email)

        uq = db.session.query(User).filter_by(email=email)
        if uq.count() == 1:
            user = uq.one()
            if user.confirm(token):
                user.name = request.form['name']
                user.password = request.form['password']
                db.session.add(user)
                db.session.commit()
                login_user(user, True)
                return redirect(url_for('main.index'))
            else:
                flash('The confirmation token is invalid.')
                return redirect(url_for('auth.register'))
        else:
            # flash no such email
            return redirect(url_for('auth.register'))
    else:
        return render_template('auth/confirm.html', token=token, email=email)


def _validate(data, fields):
    missing = []
    for field in fields:
        if data[field] == "":
            missing.append(field)
    return missing