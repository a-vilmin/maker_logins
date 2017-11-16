from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from . import auth
from .. import db
from ..email import send_email
from ..models import User, Visit
from .forms import LoginForm, RegistrationForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            if not user.in_lab:
                return redirect(request.args.get('next') or
                                url_for('main.log_visit',
                                        username=user.username))
            else:
                return redirect(request.args.get('next') or
                                url_for('main.user',
                                        username=user.username))
        # TODO FLASH MESSAGE FOR NO CLICK ON PAY BUTTON
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    flash_message = ''
    user = current_user._get_current_object()
    if not user.in_lab:
        user.in_lab = True
        db.session.commit()
        flash_message = "You're all set! Start Making!"
    else:
        user.in_lab = False
        # put leave time in to current visit
        visit = Visit.query.filter_by(visit_user=user.id)[-1]
        visit.out_time = datetime.now()
        db.session.commit()
        flash_message = "You're signed out. Thanks for visiting!"
    logout_user()
    flash(flash_message)
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,
                        user_type=form.user_type.data)
        db.session.add(new_user)
        db.session.commit()
        token = new_user.generate_confirmation_token()
        send_email(new_user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=new_user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


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


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
