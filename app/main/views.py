from flask import current_app, render_template, redirect, \
    url_for, request, abort
from flask_login import current_user, login_required
from datetime import datetime
from . import main
from .forms import VisitForm
from ..models import Visit, User
from .. import db


@main.route('/', methods=['GET', 'POST'])
@main.route('/index')
def index():
    all_users = User.query.filter(db.and_(User.in_lab == 1,
                                          User.user_type != 'staff'))

    return render_template('index.html', users=all_users)


@main.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    user = current_user._get_current_object()
    all_users = User.query.filter(db.and_(User.in_lab == 1,
                                          User.user_type != 'staff'))
    if user.username != username:
        abort(500)
    return render_template('user.html', user=user, all_users=all_users)


@main.route('/log_visit/<username>', methods=['GET', 'POST'])
@login_required
def log_visit(username):
    form = VisitForm()
    user = current_user._get_current_object()
    all_users = all_users = User.query.filter(db.and_(User.in_lab == 1,
                                                      User.user_type ==
                                                      'staff'))
    if user.username != username:
        abort(500)
    if form.validate_on_submit():
        visit = Visit(purpose=form.purpose.data,
                      visit_user=user.id,
                      in_time=datetime.now(),
                      type_visit=form.type_visit.data)

        db.session.add(visit)
        db.session.commit()
        return redirect(url_for('main.user', username=username))
    return render_template('log_visit.html', user=user, all_users=all_users)


@main.route('/user/<username>/admin_logout', methods=['GET'])
@login_required
def admin_logout(username):
    user = current_user._get_current_object()
    if user.user_type != 'staff':
        abort(500)

    loggin_out = User.query.filter_by(username=username).first()
    loggin_out.in_lab = False
    loggin_out.out_time = datetime.now()
    all_users = User.query.filter(db.and_(User.in_lab == 1,
                                          User.user_type != 'staff'))
    return render_template('user.html', user=user, all_users=all_users)


@main.route('/user/admin_logout_all', methods=['GET'])
@login_required
def admin_logout_all():
    user = current_user._get_current_object()
    if user.user_type != 'staff':
        abort(500)

    all_users = User.query.filter(db.and_(User.in_lab == 1,
                                          User.user_type != 'staff'))
    for each in all_users:
        each.in_lab = False
        each.out_time = datetime.now()

    return render_template('user.html', user=user, all_users=all_users)
